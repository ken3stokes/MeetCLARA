document.addEventListener('DOMContentLoaded', function() {
    // Password strength analyzer
    const passwordInput = document.getElementById('passwordInput');
    const strengthMeter = document.getElementById('strengthMeter');
    const strengthBar = document.getElementById('strengthBar');
    const strengthLabel = document.getElementById('strengthLabel');
    const strengthChecks = document.getElementById('strengthChecks');

    // Strength check criteria
    const strengthCriteria = [
        { id: 'length', label: 'At least 12 characters', check: (pwd) => pwd.length >= 12 },
        { id: 'uppercase', label: 'Contains uppercase letter', check: (pwd) => /[A-Z]/.test(pwd) },
        { id: 'lowercase', label: 'Contains lowercase letter', check: (pwd) => /[a-z]/.test(pwd) },
        { id: 'number', label: 'Contains number', check: (pwd) => /\d/.test(pwd) },
        { id: 'special', label: 'Contains special character', check: (pwd) => /[^A-Za-z0-9]/.test(pwd) },
        { id: 'noCommon', label: 'Not a common pattern', check: (pwd) => !hasCommonPattern(pwd) }
    ];

    // Initialize strength checks
    strengthCriteria.forEach(criteria => {
        const checkDiv = document.createElement('div');
        checkDiv.className = 'flex items-center space-x-2';
        checkDiv.innerHTML = `
            <span id="${criteria.id}-icon" class="text-gray-500">○</span>
            <span class="text-gray-300">${criteria.label}</span>
        `;
        strengthChecks.appendChild(checkDiv);
    });

    // Password input handler
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        if (password) {
            strengthMeter.classList.remove('hidden');
            updateStrengthMeter(password);
        } else {
            strengthMeter.classList.add('hidden');
        }
    });

    function updateStrengthMeter(password) {
        let score = 0;
        
        // Update each criteria check
        strengthCriteria.forEach(criteria => {
            const passed = criteria.check(password);
            const icon = document.getElementById(`${criteria.id}-icon`);
            if (passed) {
                icon.textContent = '✓';
                icon.className = 'text-green-500';
                score++;
            } else {
                icon.textContent = '○';
                icon.className = 'text-gray-500';
            }
        });

        // Calculate percentage and update visual elements
        const percentage = (score / strengthCriteria.length) * 100;
        strengthBar.style.width = `${percentage}%`;
        
        // Update color and label based on score
        let color, label;
        if (percentage <= 33) {
            color = '#ef4444';
            label = 'Weak';
        } else if (percentage <= 66) {
            color = '#eab308';
            label = 'Moderate';
        } else {
            color = '#22c55e';
            label = 'Strong';
        }
        
        strengthBar.style.backgroundColor = color;
        strengthLabel.textContent = label;
        strengthLabel.style.color = color;
    }

    // Common pattern detection
    function hasCommonPattern(password) {
        const commonPatterns = [
            /^[A-Za-z]+\d+$/, // Letters followed by numbers
            /^[A-Za-z]+[0-9!@#$%^&*]+$/, // Letters followed by symbols/numbers
            /qwerty/i,
            /asdf/i,
            /1234/,
            /password/i,
            /admin/i
        ];
        
        return commonPatterns.some(pattern => pattern.test(password));
    }

    // Initialize password manager comparison table
    const comparisonData = [
        { feature: 'Cross-platform sync', browser: '❌', manager: '✓' },
        { feature: 'Password generation', browser: '✓', manager: '✓' },
        { feature: 'Security alerts', browser: '❌', manager: '✓' },
        { feature: 'Secure sharing', browser: '❌', manager: '✓' },
        { feature: 'Encryption', browser: '✓', manager: '✓' },
        { feature: 'Auto-fill', browser: '✓', manager: '✓' },
        { feature: '2FA support', browser: '❌', manager: '✓' },
        { feature: 'Security audit', browser: '❌', manager: '✓' }
    ];

    const comparisonTable = document.getElementById('comparisonTable');
    comparisonData.forEach(row => {
        const tr = document.createElement('tr');
        tr.className = 'border-b border-gray-700';
        tr.innerHTML = `
            <td class="py-3 px-4 text-gray-300">${row.feature}</td>
            <td class="py-3 px-4 text-center">${row.browser}</td>
            <td class="py-3 px-4 text-center">${row.manager}</td>
        `;
        comparisonTable.appendChild(tr);
    });
});
