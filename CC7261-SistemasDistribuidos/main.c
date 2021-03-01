#include "TestaPrimo.h"
#include <time.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

#define N_RUNS 30
#define DEBUG 0 // 0 False | 1 True

/**
 * answer struct abstracts if 
 * a number is prime and stores the 
 * collected times and time related statistics
**/ 
struct answer {
    int isprime;
    double times[N_RUNS];
    double mean;
    double std_dev;
    double sum;
};

/**
 * Translate int to char (auxiliary function)
**/ 
char* PrimoInt2Char(int primo){
    if (primo == 0){
        return (char*)"Nao primo";
    }
    if (primo == 1){
        return (char*)"Primo";
    }
    return (char*)"Unknown";
}

/**
 * Initialize the values in a answer struct
**/
void Initialize(struct answer* ans){
    int i;
    
    ans->isprime = -1;
    for (i=0; i<N_RUNS; i++){
        ans->times[i] = -1;
    }
    ans->mean = -1;
    ans->std_dev = -1;
    ans->sum = 0;
    
}

/**
 * Calculate and fills in the
 * standard deviation for a answer struct
**/
void CalcStdDev(struct answer* ans){
    int i;
    double std_dev = 0.0;

    for (i=0; i<N_RUNS; i++){
        std_dev += pow(ans->times[i] - ans->mean, 2);
    }
    ans->std_dev = sqrt(std_dev / N_RUNS);
}

/**
 * Test if a number is prime
 * 
 * Function developed by
 * Ricardo de Carvalho Destro at 12/08/20
**/
int TestaPrimo(int n) {
    int EhPrimo = 1,
        d=2;
    if (n <= 1)
    EhPrimo = 0;

    while (EhPrimo == 1 && d <= n /2) {
        if (n % d  == 0)
            EhPrimo = 0;
        d = d + 1;
    }
    return EhPrimo;
}

int main(int argc, char** argv){
    // Declarations
    clock_t start, finish;
    struct answer answers[8];
    int i, j;

    // Test numbers
    long int test_numbers[8] = {
        7,
        37,
        8431,
        13033,
        524287,
        664283,
        3531271,
        2147483647
    };

    // Numbers loop
    for (i = 0; i < 8; i++) {
        Initialize(answers+i);

        // loop para pegar os tempos
        for (j = 0; j < N_RUNS; j++) {
            // Test if is prime and get time
            start = clock();
            answers[i].isprime = TestaPrimo(test_numbers[i]);
            finish = clock();

            // Save time
            answers[i].times[j] = (double)(finish - start) / CLOCKS_PER_SEC * 1000;

            // Cumulative variable for posterior mean calculation
            answers[i].sum += answers[i].times[j];

            // DEBUG mode prints every step
            if (DEBUG){
                printf("%d [%d/%d] -> %s (%f ms)\n", 
                    test_numbers[i],
                    j+1, 
                    N_RUNS, 
                    PrimoInt2Char(answers[i].isprime), 
                    answers[i].times[j]
                );
            }
        }

        // mean = sum / N_RUNS
        answers[i].mean = answers[i].sum / N_RUNS;
        // Standard deviation
        CalcStdDev(answers+i);

        // Print the results 
        printf(">>> Valor: %d => %s ( %f +- %f [ms] )\n\n", 
            test_numbers[i],
            PrimoInt2Char(answers[i].isprime),
            answers[i].mean, 
            answers[i].std_dev
        );
    }
    
    return 0;
}