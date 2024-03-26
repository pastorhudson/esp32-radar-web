document.addEventListener('DOMContentLoaded', function() {
    fetch('/storage/FormationFlight-latest-release-bin-assets/release.txt')
    .then(response => response.text())
    .then(data => {
        const releaseData = parseReleaseData(data);
        document.getElementById('release-version').innerText = releaseData.version;
        document.getElementById('notes-content').innerHTML = releaseData.notes;
        document.getElementById('release-notes').style.display = 'none'; // Hide notes by default
    });

    document.getElementById('toggleNotes').addEventListener('click', function() {
        const notesDiv = document.getElementById('release-notes');
        if (notesDiv.style.display === 'none') {
            notesDiv.style.display = 'block';
            this.textContent = 'Hide Release Notes';
        } else {
            notesDiv.style.display = 'none';
            this.textContent = 'Show Release Notes';
        }
    });
});

function parseReleaseData(data) {
    const lines = data.split('\n');
    const version = lines[0];
    let notes = '';
    // Start from line 3 to skip version and initial empty line
    for (let i = 2; i < lines.length; i++) {
        // Format for HTML
        notes += `<p>${lines[i]}</p>`;
    }
    return { version, notes: notes.trim() };
}
