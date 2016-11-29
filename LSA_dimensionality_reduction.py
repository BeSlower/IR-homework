import os
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import metrics

def dimensionality_reduction(Sigma_, V_, num_):
    V_reduced = V_[:num_]
    Sigma_reduced = np.diag(Sigma_[:num_], 0)
    doc_reduced = np.dot(Sigma_reduced, V_reduced)
    return doc_reduced


def visualization_clustering(doc_matrix, cls_label):
    dim, numSamples = doc_matrix.shape
    mark = ['or', 'og', 'ob', 'ok', 'oy']
    if dim == 1:
        for i in xrange(numSamples):
            markIndex = int(cls_label[i])
            plt.plot(doc_matrix[0, i], 0, mark[markIndex - 1], markersize=10)

    elif dim == 2:
        for i in xrange(numSamples):
            markIndex = int(cls_label[i])
            plt.plot(doc_matrix[0, i], doc_matrix[1, i], mark[markIndex - 1], markersize=10)

    elif dim == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, axisbg=(0, 0, 0), projection='3d')
        color = ['r', 'g', 'b', 'k', 'y']
        for i in xrange(numSamples):
            markIndex = int(cls_label[i])
            ax.scatter(doc_matrix[0, i], doc_matrix[1, i], doc_matrix[2, i], c=color[markIndex - 1], s=70)

    plt.show()


def main():
    # initialization
    retval = os.getcwd()
    corpus_path = retval + "/../vector_model_w_stem/corpus3/"
    word_set = {}
    term_list = []
    num_dimensionality = 25
    num_clusters = 5

    # get word list for each document
    for file_name in os.listdir(corpus_path):
        vector = {}
        file_path = corpus_path + file_name
        for line in open(file_path).read().split("\n"):
            word = line.split("\t")[0]
            if word:
                value = float(line.split("\t")[1])
                term_list.append(word)
                vector[word] = value
        word_set[file_name] = vector

    # get term list (vocabulary) based on documents
    print("------------------ Parameters Detail ---------------------")
    print("The length of total word list: " + str(len(term_list)))
    # remove duplicate
    term_list = list(set(term_list))
    print("Remove duplicate the length of vocabulary: " + str(len(term_list)))

    # generate term-document matrix and document list
    term_document_matrix = []
    doc_list = []
    ground_truth = []
    for doc_name in word_set.keys():
        vector = word_set[doc_name]
        ground_truth.append(doc_name.split("-")[0])
        term_document_vector = []
        for word_voc in term_list:
            if word_voc in vector.keys():
                value = vector[word_voc]
                term_document_vector.append(value)
            else:
                term_document_vector.append(0)
        term_document_matrix.append(term_document_vector)
        doc_list.append(doc_name)
    print("The number of document: " + str(len(doc_list)))
    print("The number of clusters: " + str(num_clusters))
    print("The dimensionality: " + str(num_dimensionality))

    term_document_matrix = np.array(term_document_matrix).transpose()
    # SVD
    U, Sigma, V = np.linalg.svd(term_document_matrix)

    # dimensionality reduction for each document
    doc_matrix_reduced = dimensionality_reduction(Sigma, V, num_dimensionality)

    # k-means clustering
    km = KMeans(n_clusters=num_clusters)
    km.fit(doc_matrix_reduced.transpose())

    # evaluate the quality of k-means clustering
    print("------------------ Clustering Result ---------------------")
    for label in range(0, num_clusters):
        for idx in range(0, len(doc_list)):
            if km.labels_[idx] == label:
                print doc_list[idx] + "\t" + str(km.labels_[idx])

    print("------------------- Evaluation Score ---------------------")
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(ground_truth, km.labels_))
    print("Completeness: %0.3f" % metrics.completeness_score(ground_truth, km.labels_))
    print("V-measure: %0.3f" % metrics.v_measure_score(ground_truth, km.labels_))
    print("Adjusted Rand-Index: %.3f"
          % metrics.adjusted_rand_score(ground_truth, km.labels_))

    # visualization the result of clustering
    visualization_clustering(doc_matrix_reduced, ground_truth)
    print("----------------------- All Set -------------------------")

if __name__ == "__main__":
    main()
