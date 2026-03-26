// Premium shared logic for SRI RATHNA STORES

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? "http://127.0.0.1:5555"
    : "/api";

// Auth State Management
const Auth = {
    getUser: () => JSON.parse(localStorage.getItem('store_user')),
    setUser: (user) => localStorage.setItem('store_user', JSON.stringify(user)),
    logout: () => {
        localStorage.removeItem('store_user');
        window.location.href = 'login.html';
    },
    checkAuth: (requiredRole) => {
        const user = Auth.getUser();
        if (!user) {
            window.location.href = 'login.html';
            return false;
        }
        if (requiredRole && user.role !== requiredRole) {
            window.location.href = user.role === 'admin' ? 'admin.html' : 'user.html';
            return false;
        }
        return true;
    }
};

// UI Components
const UI = {
    showToast: (message, type = 'success') => {
        const toast = document.createElement('div');
        toast.className = `glass animate-fade`;
        toast.style.cssText = `
            position: fixed; bottom: 20px; right: 20px;
            padding: 12px 24px; z-index: 1000;
            border-left: 4px solid var(--${type});
        `;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    },
    renderNavbar: () => {
        console.log("UI.renderNavbar version 3.0 loaded");
        const user = Auth.getUser();
        const nav = document.querySelector('.main-nav');
        if (!nav) return;

        let links = `
            <a href="index.html">Home</a>
            <a href="products.html">Products</a>
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
        `;

        if (user) {
            if (user.role === 'admin') {
                links += `<a href="admin.html">Dashboard</a>`;
                links += `<a href="admin_loans.html">Loans</a>`;
                links += `<a href="admin_customers.html">Analytics</a>`;
                links += `<a href="admin_reports.html">Reports</a>`;
            } else {
                links += `<a href="user.html">Overview</a>`;
                links += `<a href="user_orders.html">My Orders</a>`;
                links += `<a href="user_due.html">Pending Dues</a>`;
            }
            links += `<a href="#" onclick="Auth.logout()">Logout</a>`;
        } else {
            links += `<a href="login.html">Login</a>`;
        }

        nav.innerHTML = links;
    },
    generateReceipt: (date, items, isPending = false) => {
        // Filter items: if not isPending, only include paid items.
        const filteredItems = isPending ? items : items.filter(item => item.paid);
        
        if (filteredItems.length === 0) {
            UI.showToast("No items to generate invoice.", "warning");
            return;
        }

        const total = filteredItems.reduce((sum, item) => sum + (item.price || 0), 0);
        const gstRate = 0.05; // 5% GST included
        const subtotal = total / (1 + gstRate);
        const gstAmount = total - subtotal;
        
        const receiptWindow = window.open('', '_blank');
        const user = Auth.getUser();

        receiptWindow.document.write(`
            <html>
                <head>
                    <title>Tax Invoice - SRI RATHNA STORES - ARIYAKULAM</title>
                    <style>
                        body { font-family: 'Inter', 'Segoe UI', sans-serif; padding: 40px; color: #000; line-height: 1.4; background: #fff; }
                        .container { max-width: 800px; margin: auto; }
                        .header { display: flex; justify-content: space-between; border-bottom: 2px solid #000; padding-bottom: 20px; margin-bottom: 30px; }
                        .store-info { flex: 1; }
                        .store-name { font-size: 28px; font-weight: 900; color: #000; margin: 0; text-transform: uppercase; }
                        .gst-tag { font-weight: 700; margin-top: 5px; font-size: 14px; }
                        .invoice-meta { text-align: right; }
                        .invoice-title { font-size: 24px; font-weight: 800; color: ${isPending ? '#ef4444' : '#6366f1'}; margin: 0; }
                        .details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px; }
                        .section-title { font-weight: 800; border-bottom: 1px solid #eee; margin-bottom: 10px; font-size: 12px; text-transform: uppercase; color: #666; }
                        table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
                        th { text-align: left; background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; font-size: 12px; text-transform: uppercase; }
                        td { padding: 12px; border: 1px solid #e2e8f0; font-size: 14px; }
                        .total-section { margin-left: auto; width: 300px; }
                        .total-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }
                        .grand-total { font-weight: 900; font-size: 18px; border-top: 2px solid #000; border-bottom: 2px solid #000; padding: 12px 0; margin-top: 5px; }
                        .footer { text-align: center; margin-top: 60px; font-size: 12px; color: #666; }
                        .no-print-btn { background: #000; color: #fff; border: none; padding: 12px 30px; font-weight: 700; border-radius: 4px; cursor: pointer; margin-top: 20px; }
                        @media print { .no-print { display: none !important; } body { padding: 0; } }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <div class="store-info">
                                <div class="store-name">SRI RATHNA STORES - ARIYAKULAM</div>
                                <div class="gst-tag">GSTIN: 33CROPN7578P1ZM</div>
                                <div style="font-size: 13px; margin-top: 5px; max-width: 300px;">
                                    Thirupathur Main Road, Ariyakulam,<br>
                                    Dharmapuri
                                </div>
                                <div style="font-size: 13px;">Ph no: 9787144977</div>
                            </div>
                            <div class="invoice-meta">
                                <div class="invoice-title">${isPending ? 'DUE INVOICE' : 'TAX INVOICE'}</div>
                                <div style="margin-top: 10px; font-weight: 600;">Date: ${date}</div>
                                <div style="opacity: 0.7;">Inv No: INV-${Date.now().toString().slice(-6)}</div>
                            </div>
                        </div>

                        <div class="details-grid">
                            <div>
                                <div class="section-title">Billed To</div>
                                <div style="font-weight: 700; font-size: 16px;">${user.name || user.username}</div>
                                <div style="font-size: 14px; color: #444;">ID/Username: @${user.username}</div>
                                <div style="font-size: 14px; color: #444;">Customer Status: Registered</div>
                            </div>
                            <div style="text-align: right;">
                                <div class="section-title">Payment Info</div>
                                <div style="font-weight: 700; color: ${isPending ? '#ef4444' : '#059669'};">Payment Method: ${isPending ? 'PENDING' : 'Store Credit/Cash'}</div>
                                <div style="font-size: 14px;">Terms: ${isPending ? 'Due in 4 Days' : 'Due on Receipt'}</div>
                            </div>
                        </div>

                        <table>
                            <thead>
                                <tr>
                                    <th style="width: 50px;">S.No</th>
                                    <th>Description</th>
                                    <th style="text-align: center;">Qty</th>
                                    <th style="text-align: right;">Rate</th>
                                    <th style="text-align: right;">Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${filteredItems.map((item, i) => `
                                    <tr>
                                        <td>${i + 1}</td>
                                        <td style="font-weight: 600;">${item.product_name}</td>
                                        <td style="text-align: center;">${item.quantity || 1}</td>
                                        <td style="text-align: right;">₹${item.price / (item.quantity || 1)}</td>
                                        <td style="text-align: right; font-weight: 600;">₹${item.price}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>

                        <div class="total-section">
                            <div class="total-row">
                                <span>Taxable Amount:</span>
                                <span>₹${subtotal.toFixed(2)}</span>
                            </div>
                            <div class="total-row">
                                <span>GST (5% Included):</span>
                                <span>₹${gstAmount.toFixed(2)}</span>
                            </div>
                            <div class="total-row grand-total">
                                <span>TOTAL AMOUNT:</span>
                                <span>₹${total.toLocaleString()}</span>
                            </div>
                        </div>

                        <div class="footer">
                            <p style="font-weight: 700;">Thank you for your business!</p>
                            <p>This is a computer-generated tax invoice. No signature required.</p>
                            <div class="no-print">
                                <button class="no-print-btn" onclick="window.print()">Download as PDF / Print</button>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
        `);
        receiptWindow.document.close();
    }
};

// Data Fetching Helpers
const Api = {
    get: async (endpoint) => {
        try {
            const user = Auth.getUser();
            const headers = user ? { "Authorization": `Bearer ${user.token}` } : {};
            const r = await fetch(`${API_BASE_URL}${endpoint}`, { headers });
            if (r.status === 401) Auth.logout();
            return await r.json();
        } catch (e) {
            UI.showToast("Connection Error", "danger");
        }
    },
    post: async (endpoint, data) => {
        try {
            const user = Auth.getUser();
            const isFormData = data instanceof FormData;
            const headers = isFormData ? {} : { "Content-Type": "application/json" };
            if (user) headers["Authorization"] = `Bearer ${user.token}`;

            const r = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: "POST",
                headers: headers,
                body: isFormData ? data : JSON.stringify(data)
            });
            if (r.status === 401) Auth.logout();
            return await r.json();
        } catch (e) {
            UI.showToast("Request Failed", "danger");
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    UI.renderNavbar();
});
