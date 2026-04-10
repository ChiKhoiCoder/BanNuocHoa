/**
 * Global confirmation for destructive actions.
 *
 * Usage:
 * - Add `data-confirm="Message..."` to <a>, <button>, or <form>.
 * - For forms, message can be on the form or the submit button.
 */
(() => {
    const DEFAULT_MESSAGE = 'Bạn muốn xóa sản phẩm này không?';
    const GENERIC_MESSAGE = 'Bạn có chắc chắn muốn thực hiện thao tác này?';

    function looksDestructiveUrl(url) {
        if (!url) return false;
        const u = String(url).toLowerCase();
        // Heuristic fallback for missed places (override with data-confirm when needed)
        return /(^|[/?#_])(delete|remove|clear|cancel)(\b|[/?#_=]|$)/.test(u);
    }

    function getConfirmMessage(target, submitter) {
        return (
            (submitter && submitter.dataset && submitter.dataset.confirm) ||
            (target && target.dataset && target.dataset.confirm) ||
            null
        );
    }

    function ensureModal() {
        let modalEl = document.getElementById('confirmActionModal');
        if (!modalEl) {
            modalEl = document.createElement('div');
            modalEl.className = 'modal fade luxe-modal';
            modalEl.id = 'confirmActionModal';
            modalEl.tabIndex = -1;
            modalEl.setAttribute('aria-hidden', 'true');
            modalEl.innerHTML = `
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title"><i class="fas fa-exclamation-triangle me-2 text-warning"></i>Xác nhận</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-center py-4">
                            <p class="mb-0 fs-5" id="confirmActionModalMessage"></p>
                        </div>
                        <div class="modal-footer justify-content-center">
                            <button type="button" class="btn btn-luxe-cancel" data-bs-dismiss="modal">Hủy bỏ</button>
                            <button type="button" class="btn btn-luxe-confirm" id="confirmActionModalConfirmBtn">Xác nhận</button>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modalEl);
        }

        const messageEl = modalEl.querySelector('#confirmActionModalMessage');
        const confirmBtn = modalEl.querySelector('#confirmActionModalConfirmBtn');
        return { modalEl, messageEl, confirmBtn };
    }

    let active = null;

    function showConfirmModal(message, options = {}) {
        const msg = message || DEFAULT_MESSAGE;
        const {
            confirmText = 'Xác nhận',
            confirmBtnClass = 'btn-danger'
        } = options;

        // Prefer Bootstrap modal; fallback to native confirm if Bootstrap isn't available.
        if (!window.bootstrap || !window.bootstrap.Modal) {
            return Promise.resolve(window.confirm(msg));
        }

        const { modalEl, messageEl, confirmBtn } = ensureModal();
        messageEl.textContent = msg;

        confirmBtn.textContent = confirmText;
        // Reset classes and apply Luxe styles
        confirmBtn.className = 'btn btn-luxe-confirm';
        if (confirmBtnClass && confirmBtnClass !== 'btn-danger') {
            // If a specific non-danger class was requested, we could map it, 
            // but for Luxe we keep it gold for consistency.
        }

        if (active && active.modal) {
            // If another confirm is open, close it and resolve false.
            try {
                active.resolve(false);
                active.modal.hide();
            } catch (_) { }
        }

        const modal = window.bootstrap.Modal.getOrCreateInstance(modalEl, {
            backdrop: 'static'
        });

        return new Promise((resolve) => {
            let confirmed = false;

            const onConfirm = () => {
                confirmed = true;
                modal.hide();
            };

            const onHidden = () => {
                confirmBtn.removeEventListener('click', onConfirm);
                modalEl.removeEventListener('hidden.bs.modal', onHidden);
                active = null;
                resolve(confirmed);
            };

            confirmBtn.addEventListener('click', onConfirm);
            modalEl.addEventListener('hidden.bs.modal', onHidden, { once: true });

            active = { modal, resolve };
            modal.show();
        });
    }

    // Expose for custom JS flows (optional)
    window.confirmAction = (message, options) => showConfirmModal(message, options);

    const bypassOnce = new WeakSet();

    // Confirm clicks on links/buttons/etc. (capture to run before other handlers)
    document.addEventListener(
        'click',
        async (e) => {
            const bypassEl = e.target && e.target.closest ? e.target.closest('[data-confirm-bypass="1"]') : null;
            if (bypassEl) {
                bypassEl.removeAttribute('data-confirm-bypass');
                return;
            }

            const el = e.target && e.target.closest ? e.target.closest('[data-confirm]') : null;
            if (!el) {
                // Fallback: confirm typical destructive links even if data-confirm missing
                const a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
                if (!a) return;
                const href = a.getAttribute('href');
                if (!looksDestructiveUrl(href)) return;

                e.preventDefault();
                e.stopImmediatePropagation();

                const ok = await showConfirmModal(GENERIC_MESSAGE, { confirmText: 'Xác nhận', confirmBtnClass: 'btn-danger' });
                if (ok) {
                    a.setAttribute('data-confirm-bypass', '1');
                    window.location.href = href;
                }
                return;
            }

            // If this is a submit button inside a form, let the submit handler decide.
            if (el.tagName === 'BUTTON' && (el.getAttribute('type') || '').toLowerCase() === 'submit') return;

            const msg = getConfirmMessage(el);
            if (!msg) return;

            e.preventDefault();
            e.stopImmediatePropagation();

            const ok = await showConfirmModal(msg, { confirmText: 'Xóa', confirmBtnClass: 'btn-danger' });
            if (!ok) return;

            // Re-trigger the original action exactly once
            el.setAttribute('data-confirm-bypass', '1');
            if (el.tagName === 'A' && el.getAttribute('href')) {
                window.location.href = el.getAttribute('href');
                return;
            }

            // For buttons or other elements, clicking again will run existing handlers (onclick/addEventListener)
            if (!bypassOnce.has(el)) {
                bypassOnce.add(el);
                el.click();
                bypassOnce.delete(el);
            }
        },
        true
    );

    // Confirm form submissions (capture)
    document.addEventListener(
        'submit',
        async (e) => {
            const form = e.target;
            if (!form || form.tagName !== 'FORM') return;

            if (form.hasAttribute('data-confirm-bypass')) {
                form.removeAttribute('data-confirm-bypass');
                return;
            }

            const submitter = e.submitter || null;
            const msg = getConfirmMessage(form, submitter);
            if (!msg) {
                const method = (form.getAttribute('method') || 'get').toLowerCase();
                const action = form.getAttribute('action') || form.action;
                if (method === 'post' && looksDestructiveUrl(action)) {
                    e.preventDefault();
                    e.stopImmediatePropagation();

                    const ok = await showConfirmModal(GENERIC_MESSAGE, { confirmText: 'Xác nhận', confirmBtnClass: 'btn-danger' });
                    if (!ok) return;

                    form.setAttribute('data-confirm-bypass', '1');
                    if (submitter && form.requestSubmit) form.requestSubmit(submitter);
                    else form.submit();
                }
                return;
            }

            e.preventDefault();
            e.stopImmediatePropagation();

            const ok = await showConfirmModal(msg, { confirmText: 'Xóa', confirmBtnClass: 'btn-danger' });
            if (!ok) return;

            form.setAttribute('data-confirm-bypass', '1');
            if (submitter && form.requestSubmit) form.requestSubmit(submitter);
            else form.submit();
        },
        true
    );
})();

