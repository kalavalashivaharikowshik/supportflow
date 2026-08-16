import Button from "./Button";
import Modal from "./Modal";


function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  variant = "primary",
  loading = false,
  onConfirm,
  onCancel,
}) {
  return (
    <Modal
      open={open}
      title={title}
      description={
        message
      }
      onClose={
        loading
          ? () => {}
          : onCancel
      }
      size="sm"
      closeOnBackdrop={
        !loading
      }
      closeOnEscape={
        !loading
      }
    >
      <p
        className="
          text-sm leading-6
          text-slate-600
        "
      >
        Please confirm before
        continuing.
      </p>

      <div
        className="
          mt-6 flex
          flex-col-reverse
          gap-3
          sm:flex-row
          sm:justify-end
        "
      >
        <Button
          variant="secondary"
          disabled={loading}
          onClick={
            onCancel
          }
          className="
            w-full sm:w-auto
          "
        >
          {cancelLabel}
        </Button>

        <Button
          variant={
            variant
          }
          loading={loading}
          onClick={
            onConfirm
          }
          className="
            w-full sm:w-auto
          "
        >
          {confirmLabel}
        </Button>
      </div>
    </Modal>
  );
}


export default ConfirmDialog;