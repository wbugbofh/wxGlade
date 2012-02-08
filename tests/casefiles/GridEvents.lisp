
;;; generated by wxGlade "faked test version"

(asdf:operate 'asdf:load-op 'wxcl)
(use-package "FFI")
(ffi:default-foreign-language :stdc)

(use-package :wxEvent)
(use-package :wxFrame)
(use-package :wxWindow)
(use-package :wx_wrapper)
(use-package :wxEvtHandler)
(use-package :wxGrid)
(use-package :wx_main)
(use-package :wxCL)
(use-package :wxColour)
(use-package :wxSizer)

(defclass MyFrame()
        ((top-window :initform nil :accessor slot-top-window)
        (grid-1 :initform nil :accessor slot-grid-1)
        (sizer-1 :initform nil :accessor slot-sizer-1)))

(defun make-MyFrame ()
        (let ((obj (make-instance 'MyFrame)))
          (init obj)
          (set-properties obj)
          (do-layout obj)
          obj))

(defmethod init ((obj MyFrame))
"Method creates the objects contained in the class."
        ;;;begin wxGlade: MyFrame.__init__
        (setf (slot-top-window obj) (wxFrame_create nil -1 "" -1 -1 -1 -1 wxDEFAULT_FRAME_STYLE))
        (setf (slot-grid-1 obj) (wxGrid_Create (slot-top-window obj) -1 -1 -1 -1 -1 wxWANTS_CHARS))

        (wxEvtHandler_Connect (slot-top-window obj) obj.grid-1 (expwxEVT_GRID_CMD_CELL_LEFT_CLICK)
        (wxClosure_Create #'myEVT_GRID_CELL_LEFT_CLICK obj))
        )
        ;;; end wxGlade

(defmethod set-properties ((obj MyFrame))
        ;;;begin wxGlade: MyFrame.__set_properties
        (wxGrid_CreateGrid (slot-grid-1 obj) 10 3 0)
        (wxGrid_SetSelectionMode (slot-grid-1 obj) wxGridSelectCells)
        )
;;;end wxGlade

(defmethod do-layout ((obj MyFrame))
        ;;;begin wxGlade: MyFrame.__do_layout
        (setf (slot-sizer-1 obj) (wxBoxSizer_Create  wxVERTICAL))
        (wxSizer_AddWindow (slot-sizer-1 obj) (slot-grid-1 obj) 1 wxEXPAND 0 nil)
        (wxWindow_SetSizer (slot-top-window obj) (slot-sizer-1 obj))
        (wxSizer_Fit (slot-sizer-1 obj) (slot-top-window obj))
        )
;;;end wxGlade

(defun myEVT_GRID_CELL_LEFT_CLICK (function data event) ;;;wxGlade: MyFrame.<event_handler>
        (print "Event handler `myEVT_GRID_CELL_LEFT_CLICK' not implemented!")
        (when event
                (wxEvent:wxEvent_Skip event)))

;;; end of class MyFrame


(defun init-func (fun data evt)
    (let ((frame-1 (make-MyFrame)))
    (ELJApp_SetTopWindow (slot-top-window frame-1))
    (wxWindow_Show (slot-top-window frame-1))))

(unwind-protect
    (Eljapp_initializeC (wxclosure_Create #'init-func nil) 0 nil)
    (ffi:close-foreign-library "../miscellaneous/wxc-msw2.6.2.dll"))
