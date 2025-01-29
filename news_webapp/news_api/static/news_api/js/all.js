document.addEventListener('DOMContentLoaded', function() {
    const textElements = document.querySelectorAll('a.news-link, .custom-article, .description, p, .title');
    // persian or english
    textElements.forEach(element => {
        const textContent = element.innerText || element.textContent;


        if (/[\u0600-\u06FF]/.test(textContent)) {
            element.classList.add('rtl');
            element.classList.remove('ltr');
        } else {
            element.classList.add('ltr');
            element.classList.remove('rtl');
        }
    });


    // dark or light
    const themeToggleButton = document.getElementById("themeToggle");
    const sunIcon = document.getElementById("sunIcon");
    const moonIcon = document.getElementById("moonIcon");

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        sunIcon.classList.remove("hidden");
        moonIcon.classList.add("hidden");
    } else {
        document.body.classList.remove("dark-mode");
        sunIcon.classList.add("hidden");
        moonIcon.classList.remove("hidden");
    }

    themeToggleButton.onclick = function() {
        if (document.body.classList.contains("dark-mode")) {
            document.body.classList.remove("dark-mode");
            document.body.classList.add("light-mode");
            sunIcon.classList.add("hidden");
            moonIcon.classList.remove("hidden");
            localStorage.setItem("theme", "light");
        } else {
            document.body.classList.remove("light-mode");
            document.body.classList.add("dark-mode");
            sunIcon.classList.remove("hidden");
            moonIcon.classList.add("hidden");
            localStorage.setItem("theme", "dark");
        }
    };

    // view count
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('news-link')) {
            e.preventDefault();
    
            let newsId = e.target.getAttribute('data-news-id');
            console.log(typeof(newsId));
            console.log(newsId);
    
            fetch(`/increment_view_count/${newsId}/`, {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                let articleCard = e.target.closest('.article-card') || e.target.closest('.article-card-category');
                if (articleCard) {
                    let viewsElement = articleCard.querySelector('.views');
                    if (viewsElement) {
                        viewsElement.textContent = `Views ${data.view_count}`;
                    }
                }
                window.open(e.target.getAttribute('href'), '_blank');
            });
        }
    });
    




    function updateNews() {
        fetch('/api/update-news/')
            .then(response => response.json())
            .then(data => {
                const articlesContainer = document.querySelector('.category-bound');
                if (articlesContainer) {
                    articlesContainer.innerHTML = '';
            
                    for (const [category, articles] of Object.entries(data.category_news)) {
                        
                        const hole = document.createElement('div');
                        hole.classList.add('hole');
            
                        const categoryLink = document.createElement('a');
                        categoryLink.href = `/category/${category}`;
                        categoryLink.innerHTML = `
                            <h2 id="category-${category}" class="category">
                                ${category} <i class="bx bx-chevron-right"></i>
                            </h2>
                        `;
                        hole.appendChild(categoryLink);
            
                        articles.forEach(article => {
                            const articleCard = document.createElement('div');
                            articleCard.classList.add('article-card');
                            articleCard.innerHTML = `
                                <div class="title">
                                    <a class="news-link" target="_blank" href="${article.news_url}" data-news-id="${article.id}">
                                        ${article.title}
                                    </a>
                                    <p>${formatDate(article.published_at)}</p>
                                    <p class="views"> Views ${article.view_count}</p>
                                </div>
                                <div class="image">
                                    <img src="${article.image_url}" alt="" />
                                </div>
                            `;
                            hole.appendChild(articleCard);
                        });
            
                        articlesContainer.appendChild(hole);
                    }
                }
            })
            .catch(error => console.error('Error updating news:', error));

            
    }
    if (window.location.pathname === '/') {
        setInterval(updateNews, 3000);
    }




    
    function updateCategoryNews() {
        const pathParts = window.location.pathname.split('/');  
        const category = pathParts[2]; 
        console.log('Category:', category);
    
        if (category) {
            fetch(`/api/update-category/${category}/`)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    const articlesContainer = document.querySelector('.hole-category'); 
                    if (articlesContainer) {
                        articlesContainer.innerHTML = '';
    
                        const categoryNews = data.news;
                        categoryNews.forEach(article => {
                            const articleCard = document.createElement('div');
                            articleCard.classList.add('article-card-category'); 
                            articleCard.innerHTML = `
                                <div class="title-image">
                                    <img src="${ article.image_url }" alt="">
                                    <a class="news-link" target="_blank" href="${ article.news_url }" data-news-id="${ article.id }">${ article.id } ${ article.title }</a>

                                </div>
                                <div class="desc">
                                    <p>${ article.name }</p>
                                    <p class="description">${article.description || ''}</p>
                                    <p class="content">${article.content ? article.content.slice(0, 120) + (article.content.length > 100 ? '...' : '') : ''}
                                            <a class="news-link" target="_blank" href="${article.news_url || '#'}" data-news-id="${article.id || ''}">
                                                ${article.content && (/آ|ا|ب/.test(article.content)) ? 'بیشتر بخوانید' : 'read more'}</a>
                                    </p>   
                                    <p class="publish">${formatDate(article.published_at)}</p>
                                    <p class="views"> Views ${article.view_count}</p>
                                </div>
                            `;
                            articlesContainer.appendChild(articleCard);
                        });
                    }
                })
                .catch(error => console.error('Error updating news:', error));
    
            console.log("fjsfjaklsjfkl")
        } else {
            console.error('Invalid or missing category:', category);
        }

        
    }
    
    if (window.location.pathname === '/') {
        setInterval(updateCategoryNews, 3000);
    }
    



    function formatDate(dateString) {
        const date = new Date(dateString);
        
        const options = {
            year: 'numeric',
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        };
        
        return new Intl.DateTimeFormat('en-US', options).format(date);
    }

});
