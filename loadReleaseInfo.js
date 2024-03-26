document.addEventListener('DOMContentLoaded', function() {
    fetch('/storage/FormationFlight-latest-release-bin-assets/release.txt')
    .then(response => response.text())
    .then(data => {
        const releaseData = parseReleaseData(data);
        const versionElement = document.getElementById('release-version');
        const notesContentElement = document.getElementById('notes-content');
        const releaseNotesDiv = document.getElementById('release-notes');

        if (versionElement) versionElement.innerText = releaseData.version;
        if (notesContentElement) notesContentElement.innerHTML = releaseData.notes;
        if (releaseNotesDiv) releaseNotesDiv.style.display = 'none'; // Hide notes by default
    });

    const toggleButton = document.getElementById('toggleNotes');
    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            const notesDiv = document.getElementById('release-notes');
            if (notesDiv) {
                if (notesDiv.style.display === 'none') {
                    notesDiv.style.display = 'block';
                    this.textContent = 'Hide Release Notes';
                } else {
                    notesDiv.style.display = 'none';
                    this.textContent = 'Show Release Notes';
                }
            }
        });
    }
});

function parseReleaseData(data) {
    const lines = data.split('\n');
    const version = lines[0];
    let notes = '';
    // Start from line 3 to skip version and initial empty line
    for (let i = 2; i < lines.length; i++) {
        notes += `<p>${lines[i]}</p>`;
    }
    return { version, notes: notes.trim() };
}
