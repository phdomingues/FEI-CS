import json

FILE_NAME = 'Chaves de Criptografia 2021.S2.txt'
DEBUG = True

class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def monobit_test(bin_string):
    # Conta zeros
    X = bin_string.count("1")
    # Verifica se esta no range valido
    approved = X > 9654 and X < 10346
    return approved, X

def poker_test(bin_string):
    # Corta o string binario em pedaços de 5000 bits
    sums = {}
    n = 4
    nibles = [bin_string[i:i + n] for i in range(0, len(bin_string), n)]
    for nible in nibles:
        try: sums[nible] += 1
        except KeyError: sums[nible] = 1
    X = (16/5000) * sum(map(lambda i: int(i)**2, sums.values()))-5000
    approved = X > 1.03 and X < 57.4
    return approved, X, sums

def runs_test(bin_string):
    template = {
        1: (2267, 2733),
        2: (1079, 1421),
        3: ( 502,  748),
        4: ( 223,  402),
        5: (  90,  223),
        6: (  90,  223)
    }
    total_count = {
        0: {i: 0 for i in range(1,7)}, 
        1: {i: 0 for i in range(1,7)}
    }
    total_results = {
        0: {i: None for i in range(1,7)}, 
        1: {i: None for i in range(1,7)}
    }
    count = 1
    last = None
    for bit in bin_string:
        if bit != last:
            try: 
                count = 6 if count > 6 else count
                total_count[int(last)][count] += 1
            except (KeyError, TypeError): 
                pass # Primeira iteracao
            count = 1
            last = bit
        else:
            count += 1
    approved = True
    for bit, counts in total_count.items():
        for sequential_value, count in counts.items():
            aceito = (count > template[sequential_value][0] and count < template[sequential_value][1])
            approved = approved and aceito
            total_results[bit][sequential_value] = aceito
    return approved, total_count, total_results

def long_run_test(bin_string):
    count = 1
    last = None
    for bit in bin_string:
        if count == 34:
            return False
        if bit != last:
            count = 1
            last = bit
        else:
            count += 1
    return True

if __name__ == '__main__':
    bool2str = {True: F'{bcolors.GREEN}{bcolors.BOLD}Passou{bcolors.ENDC}', False: f'{bcolors.RED}{bcolors.BOLD}Reprovou{bcolors.ENDC}'}
    with open(FILE_NAME, 'r') as f:
        for i, line in enumerate(f):
            print("TESTANDO CHAVE ", i)
            # === Pre-Processamento
            line = line.replace("'", "")[:-1] # Remove os ' que tem no arquivo
            total_bits = len(line*4)
            # Carrega string de hex para binario
            binary_string = bin(int(line, 16))[2:].zfill(total_bits)
            # === 1. Monobit Test
            passou, X = monobit_test(binary_string)
            print(f"\t|-> MONOBIT: {bool2str[passou]} (X = {X})")
            # === 2. Poker Test
            passou, X, sums = poker_test(binary_string)
            print(f"\t|-> POKER: {bool2str[passou]} (X = {X})")
            if DEBUG: print(json.dumps(sums, sort_keys=True, indent=2))
            # === 3. Runs Test
            passou, runs_count, runs_approved = runs_test(binary_string)
            print(f"\t|-> RUNS: {bool2str[passou]}")
            if DEBUG: 
                print(json.dumps(runs_count, sort_keys=True, indent=2))
            # === 2. Poker Test
            passou = long_run_test(binary_string)
            print(f"\t|-> LONG RUN: {bool2str[passou]}")
            