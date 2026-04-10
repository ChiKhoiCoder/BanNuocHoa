/**
 * Elite Confirmation System
 * Custom high-end modal for destructive actions
 */

const EliteConfirm = {
    modal: null,
    okBtn: null,
    cancelBtn: null,
    messageEl: null,
    callback: null,

    init() {
        this.modal = document.getElementById('elite-confirm-modal');
        this.okBtn = document.getElementById('confirm-ok');
        this.cancelBtn = document.getElementById('confirm-cancel');
        this.messageEl = document.getElementById('confirm-message');

        if (!this.modal) return;

        this.okBtn.addEventListener('click', () => {
            if (this.callback) this.callback();
            this.close();
        });

        this.cancelBtn.addEventListener('click', () => {
            this.close();
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                this.close();
            }
        });

        // Initialize globally for links with .confirm-action
        this.autoBind();
    },

    show(message, onConfirm) {
        if (!this.modal) {
            // Fallback if modal not loaded
            if (confirm(message)) onConfirm();
            return;
        }

        this.messageEl.textContent = message;
        this.callback = onConfirm;
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    },

    close() {
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
        this.callback = null;
    },

    autoBind() {
        document.addEventListener('click', (e) => {
            const confirmBtn = e.target.closest('.confirm-action');
            if (confirmBtn) {
                e.preventDefault();
                const message = confirmBtn.dataset.message || 'Bạn có chắc chắn muốn thực hiện hành động này?';
                const url = confirmBtn.href;
                const form = confirmBtn.closest('form');

                this.show(message, () => {
                    if (form) {
                        form.submit();
                    } else if (url) {
                        window.location.href = url;
                    } else {
                        // Custom event for complex logic
                        confirmBtn.dispatchEvent(new CustomEvent('eliteConfirm:confirmed', { bubbles: true }));
                    }
                });
            }
        });
    }
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    EliteConfirm.init();
});
