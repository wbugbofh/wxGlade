"""
@copyright: 2012-2014 Carsten Grohmann

@license: MIT (see license.txt) - THIS PROGRAM COMES WITH NO WARRANTY
"""

# import general python modules
import StringIO
import difflib
import glob
import os.path
import re
import sys
import types
import unittest

# import project modules
import codegen
import common
import config
import log
from xml_parse import CodeWriter


class WXGladeBaseTest(unittest.TestCase):
    """\
    Provide basic functions for all tests

    All test cases uses an own implementation to L{common.save_file()} to
    catch the results. This behaviour is limited to single file creation.
    """

    vFiles = {}
    """\
    Dictionary to store the content of the files generated by the code
    generators.

    The filename is the key and the content is a StringIO instance.
    """

    orig_app_encoding = {}
    """\
    Original values for code generator app_encoding instance variable.

    @see: L{codegen.BaseLangCodeWriter.app_encoding}
    """

    orig_file_exists = None
    """\
    Reference to the original L{codegen.BaseLangCodeWriter._file_exists()}
    implementation
    """

    orig_for_version = {}
    """\
    Original values for code generator for_version instance variable.

    @see: L{codegen.BaseLangCodeWriter.for_version}
    """

    orig_load_file = None
    """\
    Reference to the original L{codegen.BaseSourceFileContent._load_file()}
    implementation
    """

    orig_os_access = None
    """\
    Reference to original C{os.access()} implementation
    
    @see: L{_os_access()}
    """

    orig_os_makedirs = None
    """\
    Reference to original C{os.makedirs()} implementation
    
    @see: L{_os_makedirs()}
    """

    orig_os_path_isdir = None
    """\
    Reference to original C{os.path.isdir()} implementation
    
    @see: L{_os_path_isdir()}
    """

    orig_save_file = None
    """\
    Reference to the original L{common.save_file()} implementation
    """

    caseDirectory = 'casefiles'
    """\
    Directory with input files and result files
    """

    @classmethod
    def setUpClass(cls):
        """\
        Initialise parts of wxGlade before individual tests starts
        """
        # set icon path back to the default default
        config.icons_path = 'icons'

        # initialise wxGlade preferences and set some useful values
        common.init_preferences()
        config.preferences.autosave = False
        config.preferences.write_timestamp = False
        config.preferences.show_progress = False

        # set own version string to prevent diff mismatches
        config.version = '"faked test version"'

        # Determinate case directory
        cls.caseDirectory = os.path.join(
            os.path.dirname(__file__),
            cls.caseDirectory,
            )

        # disable bug dialogs
        sys._called_from_test = True

    @classmethod
    def tearDownClass(cls):
        """\
        Cleanup after all individual tests are done
        """
        # de-register own logging
        log.deinit()

    def setUp(self):
        """\
        Initialise
        """
        # initiate empty structure to store files and there content
        self.vFiles = {}

        # replace some original implementations by test specific implementation
        self.orig_save_file = common.save_file
        common.save_file = self._save_file
        self.orig_load_file = codegen.BaseSourceFileContent._load_file
        codegen.BaseSourceFileContent._load_file = self._load_lines
        self.orig_file_exists = codegen.BaseLangCodeWriter._file_exists
        self.orig_os_access = os.access
        os.access = self._os_access
        self.orig_os_makedirs = os.makedirs
        os.makedirs = self._os_makedirs
        self.orig_os_path_isdir = os.path.isdir
        os.path.isdir = self._os_path_isdir
        codegen.BaseLangCodeWriter._file_exists = self._file_exists
        codegen.BaseLangCodeWriter._show_warnings = False

        # save code generator settings
        for lang in common.code_writers:
            self.orig_for_version[lang] = \
                common.code_writers[lang].for_version
            self.orig_app_encoding[lang] = \
                common.code_writers[lang].app_encoding

    def tearDown(self):
        """\
        Cleanup
        """
        # cleanup virtual files
        for filename in self.vFiles:
            self.vFiles[filename].close()
        self.vFiles = {}

        # restore original implementations
        common.save_file = self.orig_save_file
        codegen.BaseSourceFileContent._load_file = self.orig_load_file
        codegen.BaseLangCodeWriter._file_exists = self.orig_file_exists
        os.access = self.orig_os_access
        os.makedirs = self.orig_os_makedirs
        os.path.isdir = self._os_path_isdir

        # restore code generator settings
        for lang in common.code_writers:
            common.code_writers[lang].for_version = \
                self.orig_for_version[lang]
            common.code_writers[lang].app_encoding = \
                self.orig_app_encoding[lang]

    def _generate_code(self, language, document, filename):
        """\
        Generate code for the given language.

        @param language: Language to generate code for
        @type language:  str
        @param document: XML document to generate code for
        @type document:  str
        @param filename: Name of the virtual output file
        @type filename:  str
        """
        self.failUnless(
            language in common.code_writers,
            "No codewriter loaded for %s" % language
            )
        self.failUnless(
            isinstance(document, types.UnicodeType),
            'Expected unicode document, got "%s"' % type(document)
        )
      
        document = self._prepare_wxg(language, document)

        # CodeWrite need UTF-8 like all XML parsers
        document = document.encode('UTF-8')

        # generate code
        CodeWriter(
            writer=common.code_writers[language],
            input=document,
            from_string=True,
            out_path=filename,
            )

        return

    def _file_exists(self, filename):
        """\
        Check if the file is a test case file

        @rtype: bool
        """
        fullpath = os.path.join(self.caseDirectory, filename)
        exists = os.path.isfile(fullpath)
        self.failIf(
            not exists,
            'Case file %s does not exist' % filename
            )
        return exists

    def _load_file(self, filename):
        """\
        Load a file need by a test case.

        @note: wxg files will be converted to unicode.

        @param filename:  Name of the file to load
        @type filename:   str
        @return:          File content
        @rtype:           str | unicode
        """
        casename, extension = os.path.splitext(filename)
        if extension == '.wxg':
            filetype = 'input'
        else:
            filetype = 'result'

        file_list = glob.glob(
            os.path.join(self.caseDirectory, "%s%s" % (casename, extension))
            )
        self.failIf(
           len(file_list) == 0,
           'No %s file "%s" for case "%s" found!' % (
                filetype,
                filename,
                casename,
                )
           )
        self.failIf(
           len(file_list) > 1,
           'More than one %s file "%s" for case "%s" found!' % (
                filetype,
                filename,
                casename,
                )
           )

        fh = open(file_list[0])
        content = fh.read()
        if extension == '.wxg':
            content = content.decode('UTF-8')
        fh.close()

        # replacing path entries
        content = content % {
            'wxglade_path':   config.wxglade_path,
            'docs_path':      config.docs_path,
            'icons_path':     config.icons_path,
            'widgets_path':   config.widgets_path,
            'templates_path': config.templates_path,
            'tutorial_file':  config.tutorial_file,
            }

        return content

    def _load_lines(self, filename):
        """\
        Return file content as a list of lines 
        """
        casename, extension = os.path.splitext(filename)
        if extension == '.wxg':
            filetype = 'input'
        else:
            filetype = 'result'

        file_list = glob.glob(
            os.path.join(self.caseDirectory, "%s%s" % (casename, extension))
            )
        self.failIf(
           len(file_list) == 0,
           'No %s file for case "%s" found!' % (filetype, casename)
           )
        self.failIf(
           len(file_list) > 1,
           'More than one %s file for case "%s" found!' % (filetype, casename)
           )

        fh = open(file_list[0])
        if extension == '.wxg':
            content = [line.decode('UTF-8') for line in fh.readlines()]
        else:
            content = fh.readlines()
        fh.close()

        return content

    def _modify_attrs(self, content, **kwargs):
        """\
        Modify general options inside a wxg (XML) file
        """
        modified = content
        for option in kwargs:
            # create regexp first
            pattern = r'%s=".*?"' % option
            modified = re.sub(
                pattern, 
                '%s="%s"' % (option, kwargs[option]),
                modified,
                1
                )

        return modified

    def _os_access(self, path, mode):
        """\
        Fake implementation for C{os.access()}
        """
        if path in ["/non-writable"]:
            return False
        return True

    def _os_makedirs(self, path, mode):
        """\
        Fake implementation for C{os.makedirs()} - do nothing
        """
        pass

    def _os_path_isdir(self, s):
        """\
        Fake implementation for C{os.path.isdir()}
        """
        if s in [".", "./", "/tmp", "/", "/non-writable"]:
            return True
        return False

    def _prepare_wxg(self, language, document):
        """\
        Set test specific options inside a wxg (XML) file

        @param language: Language to generate code for
        @type language:  str
        @param document: XML document to generate code for
        @type document:  str

        @return: Modified XML document
        @rtype:  str
        """
        _document = self._modify_attrs(
            document,
            language=language,
            indent_amount='4',
            indent_symbol='space',
        )
        return _document

    def _save_file(self, filename, content, which='wxg'):
        """\
        Test specific implementation of L{common.save_file()} to get the
        result of the code generation without file creation.

        The file content is stored in a StringIO instance. It's
        accessible at L{self.vFiles} using the filename as key.

        @note: The signature is as same as L{wxglade.common.save_file()} but
               the functionality differs.

        @param filename: Name of the file to create
        @param content:  String to store into 'filename'
        @param which:    Kind of backup: 'wxg' or 'codegen'
        """
        self.failIf(
            filename in self.vFiles,
            "Virtual file %s already exists" % filename
            )
        self.failUnless(
            filename,
            "No filename given",
            )
        outfile = StringIO.StringIO()
        outfile.write(content)
        self.vFiles[filename] = outfile

    def _test_all(self, base, excluded=None):
        """\
        Generate code for all languages based on the base file name
        
        @param base: Base name of the test files
        @type base: str
        @param excluded: Languages to exclude from test
        @type excluded:  list[str]
        """
        for lang, ext in [
            ['lisp',   '.lisp'],
            ['perl',   '.pl'],
            ['python', '.py'],
            ['XRC',    '.xrc'],
            ['C++',    ''],
            ]:
            if excluded and lang in excluded:
                continue
            name_wxg = '%s.wxg' % base
            name_lang = '%s%s' % (base, ext)
            
            if lang == 'C++':
                self._generate_and_compare_cpp(name_wxg, name_lang)
            else:
                self._generate_and_compare(lang, name_wxg, name_lang)

    def _diff(self, text1, text2):
        """\
        Compare two lists, tailing spaces will be removed

        @param text1: Expected text
        @type text1:  str
        @param text2: Generated text
        @type text2:  str

        @return: Changes formatted as unified diff
        @rtype:  str
        """
        self.assertTrue(isinstance(text1, types.StringTypes))
        self.assertTrue(isinstance(text2, types.StringTypes))

        # split into lists, because difflib needs lists and remove
        # tailing spaces
        list1 = [x.rstrip() for x in text1.splitlines()]
        list2 = [x.rstrip() for x in text2.splitlines()]

        # compare source files
        diff_gen = difflib.unified_diff(
            list1,
            list2,
            fromfile='expected source',
            tofile='created source',
            lineterm=''
            )
        return '\n'.join(diff_gen)

    def _generate_and_compare(self, lang, inname, outname):
        """\
        Generate code and compare generated and expected code

        @param lang:    Language to generate code for
        @type lang:     str
        @param inname:  Name of the XML input file
        @type inname:   str
        @param outname: Name of the output file
        @type outname:  str
        """
        # load XML input file
        source = self._load_file(inname)
        expected = self._load_file(outname)

        # generate code
        self._generate_code(lang, source, outname)
        generated = self.vFiles[outname].getvalue()
        self._compare(expected, generated)

    def _generate_and_compare_cpp(self, inname, outname):
        """\
        Generate C++ code and compare generated and expected code

        @param inname:  Name of the XML input file
        @type inname:   str
        @param outname: Name of the output file without extension
        @type outname:  str
        """
        name_h = '%s.h' % outname
        name_cpp = '%s.cpp' % outname

        # load XML input file
        source = self._load_file(inname)
        result_cpp = self._load_file(name_cpp)
        result_h = self._load_file(name_h)

        # generate and compare C++ code
        self._generate_code('C++', source, outname)
        generated_cpp = self.vFiles[name_cpp].getvalue()
        generated_h = self.vFiles[name_h].getvalue()
        self._compare(result_cpp, generated_cpp, 'C++ source')
        self._compare(result_h, generated_h, 'C++ header')

    def _compare(self, expected, generated, filetype=None):
        """\
        Compare two text documents using a diff algorithm

        @param expected:  Expected content
        @type expected:   str
        @param generated: Generated content
        @type generated:  str
        @param filetype:  Short description of the content
        @type filetype:   str
        """
        # compare files
        delta = self._diff(expected, generated)

        if filetype:
            self.failIf(
                delta,
                "Generated %s file and expected result differs:\n%s" % (
                    filetype,
                    delta,
                    )
                )
        else:
            self.failIf(
                delta,
                "Generated file and expected result differs:\n%s" % delta
                )
