from sklearn.decomposition import LatentDirichletAllocation
import sklearn.feature_extraction.text
import numpy as np


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))


def lda_top_words(input_list, top_words_number=5, topics_number=5):
    train_data = input_list

    tf_vectorizer = sklearn.feature_extraction.text.CountVectorizer(
        stop_words='english', max_df=0.95, min_df=2)
    x_train = tf_vectorizer.fit_transform(train_data)

    lda = LatentDirichletAllocation(n_topics=topics_number, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)

    reduced_train_data = lda.fit_transform(x_train).transpose()
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, top_words_number)


def key_words(input_list, top_words_number=10):
    train_data = input_list

    tf_vectorizer = sklearn.feature_extraction.text.CountVectorizer(
        stop_words='english', max_df=0.95, min_df=2)
    x_train = tf_vectorizer.fit_transform(train_data)
    feature_names = tf_vectorizer.get_feature_names()
    term_frequencies = x_train.sum(axis=0)
    array = np.asarray(term_frequencies)[0]
    count_with_index = []
    for index in xrange(len(array)):
        count_with_index.append((array[index], index))

    count_with_index.sort(key=lambda x: x[0], reverse=True)
    return [feature_names[index] for count, index in count_with_index[:top_words_number]]