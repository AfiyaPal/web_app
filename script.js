        // ── State ──
        let mode = 'signin'; // 'signin' | 'signup'
        let pwVisible = false;

        // ── DOM refs ──
        const tabSignIn    = document.getElementById('tabSignIn');
        const tabSignUp    = document.getElementById('tabSignUp');
        const nameGroup    = document.getElementById('nameGroup');
        const forgotRow    = document.getElementById('forgotRow');
        const tagline      = document.getElementById('tagline');
        const btnLabel     = document.getElementById('btnLabel');
        const submitBtn    = document.getElementById('submitBtn');
        const passwordInput= document.getElementById('passwordInput');
        const pwStrength   = document.getElementById('pwStrength');
        const pwLabel      = document.getElementById('pwLabel');
        const toast        = document.getElementById('toast');
        const logoIcon     = document.getElementById('logoIcon');

        // ── Tab switching ──
        function switchTab(tab) {
            mode = tab;
            if (tab === 'signup') {
                tabSignUp.classList.add('active');
                tabSignIn.classList.remove('active');
                nameGroup.classList.add('visible');
                forgotRow.classList.add('hidden');
                tagline.textContent = 'Start your wellness journey';
                btnLabel.textContent = 'Create Account';
            } else {
                tabSignIn.classList.add('active');
                tabSignUp.classList.remove('active');
                nameGroup.classList.remove('visible');
                forgotRow.classList.remove('hidden');
                tagline.textContent = 'Welcome back to wellness';
                btnLabel.textContent = 'Sign In';
            }
            // Reset password strength
            passwordInput.value = '';
            updateStrength('');
        }

        // ── Toggle password visibility ──
        function togglePassword() {
            pwVisible = !pwVisible;
            passwordInput.type = pwVisible ? 'text' : 'password';
            document.getElementById('eyeIcon').innerHTML = pwVisible
                ? '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>'
                : '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
        }

        // ── Password strength meter ──
        passwordInput.addEventListener('input', function () {
            updateStrength(this.value);
        });

        function updateStrength(pw) {
            let score = 0;
            if (pw.length >= 6) score++;
            if (pw.length >= 10) score++;
            if (/[A-Z]/.test(pw)) score++;
            if (/[0-9]/.test(pw)) score++;
            if (/[^A-Za-z0-9]/.test(pw)) score++;

            const colors = ['#e9ecef','#dc3545','#ffc107','#ffc107','#20c997','#28a745'];
            const labels = ['','Weak','Fair','Good','Strong','Very Strong'];

            for (let i = 1; i <= 5; i++) {
                document.getElementById('bar' + i).style.background = i <= score ? colors[score] : '#e9ecef';
            }

            if (pw.length > 0) {
                pwStrength.classList.add('visible');
                pwLabel.classList.add('visible');
                pwLabel.textContent = labels[score];
            } else {
                pwStrength.classList.remove('visible');
                pwLabel.classList.remove('visible');
            }
        }

        // ── Submit ──
        function handleSubmit(e) {
            e.preventDefault();
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;

            setTimeout(function () {
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
                showToast(mode === 'signup' ? '✓ Account created! Welcome to AfiyaPal!' : '✓ Welcome back to AfiyaPal!');
            }, 2000);
        }

        // ── Ripple effect on submit ──
        submitBtn.addEventListener('click', function (e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = (e.clientX - rect.left) + 'px';
            ripple.style.top = (e.clientY - rect.top) + 'px';
            this.appendChild(ripple);
            setTimeout(function () { ripple.remove(); }, 600);
        });

        // ── Social login ──
        function socialLogin(provider) {
            showToast('Connecting to ' + provider + '...');
        }

        // ── Toast ──
        function showToast(msg) {
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(function () { toast.classList.remove('show'); }, 3000);
        }

        // ── Logo heartbeat on hover ──
        logoIcon.addEventListener('mouseenter', function () {
            this.style.animation = 'heartbeat 0.8s ease-in-out';
        });
        logoIcon.addEventListener('animationend', function () {
            this.style.animation = '';
        });

        // ── Input focus glow on labels ──
        document.querySelectorAll('.input-group input').forEach(function (input) {
            input.addEventListener('focus', function () {
                this.parentElement.style.transform = 'translateY(-1px)';
            });
            input.addEventListener('blur', function () {
                this.parentElement.style.transform = '';
            });
        });