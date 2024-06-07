from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def file_upload(request: HttpRequest):
    if request.method == 'POST' and request.FILES.get('file_upload'):
        file = request.FILES['file_upload']
        max_size = 1

        if file.size / 1048576 > max_size:
            return HttpResponse(f'<h1>Ошибка размера файла!</h1>\n'
                                f'<h2>Файл больше, чем {max_size} мб</h2>')

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        print('Файл сохранен', filename)

    return render(request, 'requestdataapp/file-upload.html')
