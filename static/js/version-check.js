// Version checking functionality
class VersionChecker {
    constructor(currentVersion) {
        this.currentVersion = currentVersion;
        this.lastCheckKey = 'clara_version_last_check';
        this.checkIntervalDays = 7; // Check weekly
    }

    // Parse version string into comparable components
    parseVersion(versionString) {
        const match = versionString.match(/^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z]+))?/);
        if (!match) return null;
        
        return {
            major: parseInt(match[1]),
            minor: parseInt(match[2]),
            patch: parseInt(match[3]),
            preRelease: match[4] || ''
        };
    }

    // Compare two version objects
    compareVersions(v1, v2) {
        if (v1.major !== v2.major) return v1.major - v2.major;
        if (v1.minor !== v2.minor) return v1.minor - v2.minor;
        if (v1.patch !== v2.patch) return v1.patch - v2.patch;
        
        // Handle pre-release versions (alpha < beta < release)
        const preReleaseOrder = { 'alpha': 0, 'beta': 1, '': 2 };
        return (preReleaseOrder[v1.preRelease] || 0) - (preReleaseOrder[v2.preRelease] || 0);
    }

    // Check if it's time to verify version
    shouldCheck() {
        const lastCheck = localStorage.getItem(this.lastCheckKey);
        if (!lastCheck) return true;

        const daysSinceLastCheck = (Date.now() - parseInt(lastCheck)) / (1000 * 60 * 60 * 24);
        return daysSinceLastCheck >= this.checkIntervalDays;
    }

    // Update last check timestamp
    updateLastCheck() {
        localStorage.setItem(this.lastCheckKey, Date.now().toString());
    }

    // Check version against latest release
    async checkVersion() {
        if (!this.shouldCheck()) return;

        try {
            const response = await fetch('/api/version');
            const latestVersion = await response.json();
            
            const current = this.parseVersion(this.currentVersion);
            const latest = this.parseVersion(latestVersion.version);
            
            if (!current || !latest) return;

            if (this.compareVersions(current, latest) < 0) {
                this.showUpdateNotification(latestVersion);
            }

            this.updateLastCheck();
        } catch (error) {
            console.error('Version check failed:', error);
        }
    }

    // Show update notification
    showUpdateNotification(latestVersion) {
        const notification = document.createElement('div');
        notification.className = 'version-notification';
        notification.innerHTML = `
            <div class="version-notification-content">
                <p>A new version of CLARA is available (${latestVersion.version})</p>
                <p class="version-notification-description">${latestVersion.description}</p>
                <button onclick="window.location.reload()">Refresh to Update</button>
                <button class="dismiss" onclick="this.parentElement.parentElement.remove()">Dismiss</button>
            </div>
        `;
        document.body.appendChild(notification);
    }
}
