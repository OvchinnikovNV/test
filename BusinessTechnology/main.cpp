#include <QCoreApplication>
#include <iostream>

using namespace std;

void Merge(int *A, int p, int q, int r) {
    int size = r - p + 1;
    int *B = new int[size];

    int i = p - 1;  // индекс 1го подмассива
    int k = q;      // индекс 2го подмассива
    int index = 0;  // индекс new массива B

    while (i < q && k < r) {
        if (A[i] > A[k]) {
            B[index++] = A[k++];
        }
        else {
            B[index++] = A[i++];
        }
    }

    if (i == q && k < r) {
        for (; index < size; index++)
            B[index] = A[k++];
    }

    if (i < q && k == r) {
        for (; index < size; index++)
            B[index] = A[i++];
    }

    index = 0;
    for (int a = p - 1; a < r; a++)
        A[a] = B[index++];

    delete [] B;
}

void Sort(int *A, int p, int r) {
    if (p < r) {
        int q = (int)((p + r) / 2);
        Sort(A, p, q);
        Sort(A, q+1, r);
        Merge(A, p, q, r);
    }
}

void printArray(int *array, int size) {
    for(int i=0; i < size; i++)
        cout << array[i] << ' ';
    cout << endl;
}

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    int A[] = {8, 13, 4, 0, -4, 1, 13};
    int size = sizeof(A) / sizeof(A[0]);

    printArray(A, size);
    Sort(A, 1, size);
    printArray(A, size);

    return a.exec();
}
