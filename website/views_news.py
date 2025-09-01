from django.shortcuts import render

def news_page(request):
    # You can later fetch news from a model or API
    news_list = [
        {'title': 'Welcome to Hamro Engineering!', 'date': '2025-09-01', 'content': 'We are live with new features.'},
        {'title': 'Mock Test Series Launched', 'date': '2025-08-25', 'content': 'Try our new mock test series for entrance preparation.'},
    ]
    return render(request, 'news.html', {'news_list': news_list})
