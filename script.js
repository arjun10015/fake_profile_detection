async function analyze() {
    const fileInput = document.getElementById('csvFile');
    const resultsDiv = document.getElementById('results');
    const loader = document.getElementById('loader');
    const tableBody = document.querySelector('#resultTable tbody');
    const statsDiv = document.getElementById('stats');

    if (!fileInput.files[0]) {
        alert('Please select a CSV file first!');
        return;
    }

    try {
        loader.style.display = 'block';
        resultsDiv.style.display = 'none';

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        // Update stats
        statsDiv.innerHTML = `
            <div class="stat-item">
                <h3>${data.stats.total}</h3>
                <p>Total Profiles</p>
            </div>
            <div class="stat-item">
                <h3 style="color: #e74c3c;">${data.stats.fake_count}</h3>
                <p>Fake Detected</p>
            </div>
            <div class="stat-item">
                <h3 style="color: ${data.stats.risk_level === 'High' ? '#e74c3c' : '#2ecc71'};">${data.stats.risk_level}</h3>
                <p>Risk Level</p>
            </div>
        `;

        // Update table
        tableBody.innerHTML = data.fake_profiles.map(profile => `
            <tr>
                <td>${profile.username || 'N/A'}</td>
                <td>${profile.email || 'N/A'}</td>
                <td>${profile.join_date || 'N/A'}</td>
                <td><span class="risk-badge">${profile.risk_score || 'High'}</span></td>
            </tr>
        `).join('');

        resultsDiv.style.display = 'block';
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        loader.style.display = 'none';
    }
}