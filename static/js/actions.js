document.addEventListener('DOMContentLoaded', function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    document.querySelectorAll('.rate-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const pk = this.dataset.pk;
            const val = this.dataset.value;
            
            fetch(`/${pk}/rate/${val}/`, {
                method: 'POST',
                headers: { 
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => {
                if (!res.ok) throw new Error('404 or Server Error');
                return res.json();
            })
            .then(data => {
                document.getElementById('rating-display').innerText = data.rating;
            })
            .catch(err => console.error('Error:', err));
        });
    });

    const bookmarkBtn = document.getElementById('bookmark-btn');
    if (bookmarkBtn) {
        bookmarkBtn.addEventListener('click', function() {
            const pk = this.dataset.pk;
            fetch(`/${pk}/bookmark/`, {
                method: 'POST',
                headers: { 
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => {
                if (!res.ok) throw new Error('404 or Server Error');
                return res.json();
            })
            .then(data => {
                
                if (data.bookmarked) {
                    this.innerText = '🔖 Saved';
                    this.classList.add('btn-active');
                    this.classList.remove('btn-outline');
                } else {
                    this.innerText = '🔖 Bookmark';
                    this.classList.remove('btn-active');
                    this.classList.add('btn-outline');
                }
            })
            .catch(err => console.error('Error:', err));
        });
    }
});