from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import string

# Загрузка стоп-слов
nltk.download('stopwords')
stop_words = stopwords.words('russian') + stopwords.words('english')  # Можно выбрать язык


# === Функция обработки текста ===
def extract_keywords(text, top_n=10):
    # Очистка текста
    text = text.lower().translate(str.maketrans('', '', string.punctuation))

    # Векторизация TF-IDF
    vectorizer = TfidfVectorizer(stop_words=stop_words, ngram_range=(1, 2))  # 1- и 2-граммы
    tfidf_matrix = vectorizer.fit_transform([text])

    # Получаем слова и их веса
    feature_array = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Соединяем и сортируем
    word_score_pairs = list(zip(feature_array, tfidf_scores))
    sorted_keywords = sorted(word_score_pairs, key=lambda x: x[1], reverse=True)

    # Вывод
    print("🔑 Топ ключевых слов и фраз:")
    for word, score in sorted_keywords[:top_n]:
        print(f"{word:<25} — вес: {score:.4f}")


# === Пример использования ===
if __name__ == "__main__":
    text_input = input("Введите текст: ")
    extract_keywords(text_input, top_n=10)
