#include "TestaPrimo.h"
#include <time.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

#define N_RUNS 1
#define DEBUG 0 // 0 False | 1 True
#define PRIME_FUNCTION TestaPrimo_6k1

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
        return (char*)"Nao";
    }
    if (primo == 1){
        return (char*)"Sim";
    }
    return (char*)"???";
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
 * Calculate the speed up
**/
double SpeedUp(double old_value, double new_value){
    if (new_value == 0) return NAN;
    return old_value / new_value;
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

/**
 * Basic sqrt optimization for the
 * TestaPrimo function
**/
int TestaPrimo_sqrt(int n) {
    // every number <2 is not prime
    if (n < 2) {
        return 0;
    } 
    // 2 and 3 are prime
    if (n < 4) {
        return 1;
    }

    int i = 5;
    double max = sqrt(n);
    while (i < max){
        if ((n % i) == 0) {
            return 0;
        }
        i += 2;
    }

    return 1;
}

/**
 * Primality test with 6k+-1 optimization.
**/
int TestaPrimo_6k1(int n)
{
    if (n == 2 || n == 3) { 
        return 1; 
    }
    else if (n <= 1 || (n % 2) == 0 || (n % 3) == 0) { 
        return 0; 
    }
    
    int i = 5;
    double max = sqrt(n);
    while (i <= max)
    {
        if ((n % i) == 0 || (n % (i + 2)) == 0) { 
            return 0; 
        }
        i += 6;
    }
    
    return 1;
}

struct answer RunTest(int (*primeFunctionPtr)(int), const long int test_number){
    int i;
    clock_t start, finish;
    struct answer ans;
    Initialize(&ans);

    // loop para pegar os tempos
    for (i = 0; i < N_RUNS; i++) {
        // Test if is prime and get time
        start = clock();
        ans.isprime = (*primeFunctionPtr)(test_number);
        finish = clock();

        // Save time
        ans.times[i] = (double)(finish - start) / CLOCKS_PER_SEC * 1000;

        // Cumulative variable for posterior mean calculation
        ans.sum += ans.times[i];

        // DEBUG mode prints every step
        if (DEBUG){
            printf("num = %ld [%d/%d] -> %s (%f ms)\n", 
                test_number,
                i+1, 
                N_RUNS, 
                PrimoInt2Char(ans.isprime), 
                ans.times[i]
            );
        }
    }

        // mean = sum / N_RUNS
        ans.mean = ans.sum / N_RUNS;
        // Standard deviation
        CalcStdDev(&ans);

        return ans;
}

int main(int argc, char** argv){
    // Declarations
    int i;
    struct answer testa_primo_results[8];
    struct answer testa_primo_sqrt_results[8];
    struct answer testa_primo_6k1_results[8];

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
        if (DEBUG) printf("\n\n\n######################\n##### TestaPrimo #####\n######################\n\n");
        testa_primo_results[i] = RunTest(TestaPrimo, test_numbers[i]);
        if (DEBUG) printf("\n\n\n###########################\n##### TestaPrimo_sqrt #####\n###########################\n\n");
        testa_primo_sqrt_results[i] = RunTest(TestaPrimo_sqrt, test_numbers[i]);
        if (DEBUG) printf("\n\n\n##########################\n##### TestaPrimo_6k1 #####\n##########################\n\n");
        testa_primo_6k1_results[i] = RunTest(TestaPrimo_6k1, test_numbers[i]);
    }

    if (DEBUG) printf("\n\n>>> RESULTADOS <<<\n\n");
    // Result table 1 - TestaPrimo
    printf("|------------|-------|------------|------------|\n");
    printf("|   Valor    | Primo | Media [ms] | Desv. Pad. |\n");
    printf("|------------|-------|------------|------------|\n");
    for (i=0; i<8; i++){
        printf("| %-10ld |  %s  | %-10.2f | %-10.2f |\n",
            test_numbers[i], 
            PrimoInt2Char(testa_primo_results[i].isprime), 
            testa_primo_results[i].mean,
            testa_primo_results[i].std_dev
        );
    }
    printf("|------------|-------|------------|------------|\n\n");
    

    // Result table 2 - Compair algorithms
    printf("|------------|-----------------------|-----------------------|\n");
    printf("|            |         Media         |        SpeedUp        |\n");
    printf("|   Valor    |-----------|-----------|-----------|-----------|\n");
    printf("|            |    sqrt   |   6k+-1   |    sqrt   |   6k+-1   |\n");
    printf("|------------|-----------|-----------|-----------|-----------|\n");
    for (i=0; i<8; i++){
        printf("| %-10ld | %-9.2f | %-9.2f | %-9.2f | %-9.2f |\n",
            test_numbers[i],
            testa_primo_sqrt_results[i].mean,
            testa_primo_6k1_results[i].mean,
            testa_primo_results[i].mean / testa_primo_sqrt_results[i].mean,
            testa_primo_results[i].mean / testa_primo_6k1_results[i].mean
        );
    }
    printf("|------------|-----------|-----------|-----------|-----------|\n");
    

    return 0;
}