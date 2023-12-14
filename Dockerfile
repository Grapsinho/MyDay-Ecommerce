# operation system Windows and python version
FROM python:3.12-slim-bullseye

# ანუ ამის გამოყენებით პითონი არ დაწერს ასეთ ფაილებს .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# ყველა აუთფუთი გაიგზავნება კონტაინერის კონსოლში
ENV PYTHONUNBUFFERED 1

WORKDIR /mydayapp

COPY requirements.txt /mydayapp/
# --no-cache-dir ეს ეუბნება pipს რომ არ გამოიყენოს ქეშინგი გადმოწერის დროს 
RUN pip install --no-cache-dir -r requirements.txt

# ყველაფერს ვაკოპირებთ /app ფოლდერში
COPY . .

# ამით ვუშვებთ აპლიკაციას
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]