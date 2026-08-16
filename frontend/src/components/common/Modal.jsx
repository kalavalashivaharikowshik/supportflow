import {
  useEffect,
  useId,
  useRef,
} from "react";

import {
  X,
} from "lucide-react";


const SIZE_CLASSES = {
  sm: "max-w-md",
  md: "max-w-xl",
  lg: "max-w-3xl",
  xl: "max-w-5xl",
};


function Modal({
  open,
  title,
  description,
  children,
  onClose,
  size = "md",
  closeOnBackdrop = true,
  closeOnEscape = true,
}) {
  const dialogRef =
    useRef(null);

  const previousFocusRef =
    useRef(null);

  const titleId =
    useId();

  const descriptionId =
    useId();


  useEffect(() => {
    if (!open) {
      return undefined;
    }

    previousFocusRef.current =
      document.activeElement;


    const dialog =
      dialogRef.current;


    const getFocusableElements =
      () => {
        if (!dialog) {
          return [];
        }

        return Array.from(
          dialog.querySelectorAll(
            [
              "button:not([disabled])",
              "a[href]",
              "input:not([disabled])",
              "select:not([disabled])",
              "textarea:not([disabled])",
              '[tabindex]:not([tabindex="-1"])',
            ].join(",")
          )
        );
      };


    const focusableElements =
      getFocusableElements();

    if (
      focusableElements.length > 0
    ) {
      focusableElements[0].focus();
    } else {
      dialog?.focus();
    }


    const handleKeyDown =
      (event) => {
        if (
          event.key === "Escape" &&
          closeOnEscape
        ) {
          event.preventDefault();
          onClose();
          return;
        }


        if (
          event.key !== "Tab"
        ) {
          return;
        }


        const items =
          getFocusableElements();


        if (
          items.length === 0
        ) {
          event.preventDefault();
          dialog?.focus();
          return;
        }


        const first =
          items[0];

        const last =
          items[
            items.length - 1
          ];


        if (
          event.shiftKey &&
          document.activeElement ===
            first
        ) {
          event.preventDefault();

          last.focus();
        } else if (
          !event.shiftKey &&
          document.activeElement ===
            last
        ) {
          event.preventDefault();

          first.focus();
        }
      };


    document.addEventListener(
      "keydown",
      handleKeyDown
    );


    const previousOverflow =
      document.body.style.overflow;

    document.body.style.overflow =
      "hidden";


    return () => {
      document.removeEventListener(
        "keydown",
        handleKeyDown
      );

      document.body.style.overflow =
        previousOverflow;

      previousFocusRef.current
        ?.focus?.();
    };
  }, [
    open,
    onClose,
    closeOnEscape,
  ]);


  if (!open) {
    return null;
  }


  return (
    <div
      className="
        fixed inset-0 z-[100]
        flex items-center
        justify-center
        bg-slate-950/50
        p-4
      "
      onMouseDown={
        (event) => {
          if (
            closeOnBackdrop &&
            event.target ===
              event.currentTarget
          ) {
            onClose();
          }
        }
      }
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={
          titleId
        }
        aria-describedby={
          description
            ? descriptionId
            : undefined
        }
        tabIndex={-1}
        className={`
          max-h-[90vh]
          w-full
          overflow-y-auto
          rounded-2xl
          bg-white
          shadow-2xl
          outline-none
          ${
            SIZE_CLASSES[size] ??
            SIZE_CLASSES.md
          }
        `}
      >
        <div
          className="
            flex items-start
            justify-between
            gap-4 border-b
            border-slate-200
            px-6 py-5
          "
        >
          <div
            className="min-w-0"
          >
            <h2
              id={titleId}
              className="
                text-lg
                font-semibold
                text-slate-900
              "
            >
              {title}
            </h2>

            {description && (
              <p
                id={
                  descriptionId
                }
                className="
                  mt-1 text-sm
                  leading-6
                  text-slate-500
                "
              >
                {description}
              </p>
            )}
          </div>

          <button
            type="button"
            onClick={onClose}
            className="
              shrink-0
              rounded-lg p-2
              text-slate-500
              transition
              hover:bg-slate-100
              hover:text-slate-900
              focus-visible:outline-none
              focus-visible:ring-2
              focus-visible:ring-slate-400
              focus-visible:ring-offset-2
            "
            aria-label="Close dialog"
          >
            <X
              className="h-5 w-5"
            />
          </button>
        </div>

        <div
          className="
            p-6
          "
        >
          {children}
        </div>
      </div>
    </div>
  );
}


export default Modal;