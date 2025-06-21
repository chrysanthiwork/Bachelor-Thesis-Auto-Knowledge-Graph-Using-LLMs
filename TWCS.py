import random
import math

# Load triplets from file
def load_triples(file_path):
    triples = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                subject, predicate, obj = line.strip().split(', ')
                if subject not in triples:
                    triples[subject] = []
                triples[subject].append((subject, predicate, obj))
            except ValueError:
                # Skip lines that don't have exactly three parts
                continue
    return triples

# Επιλογή συστάδων (clusters) με Weighted Cluster Sampling (WCS)
def weighted_cluster_sampling(triples, n):
    total_size = sum(len(cluster) for cluster in triples.values())
    probabilities = {cluster: len(triples[cluster]) / total_size for cluster in triples}
    selected_clusters = random.choices(list(triples.keys()), weights=probabilities.values(), k=n)
    return selected_clusters

# Επιλογή τριπλετών από συστάδες με το 2ο Στάδιο (TWCS)
def two_stage_sampling(triples, selected_clusters, m):
    sampled_triples = {}
    for cluster in selected_clusters:
        cluster_triples = triples[cluster]
        sample_size = min(len(cluster_triples), m)
        sampled_triples[cluster] = random.sample(cluster_triples, sample_size)
    return sampled_triples

# Υπολογισμός του Hansen-Hurwitz estimator για το TWCS
def hansen_hurwitz_twcs_estimator(sampled_triples, accuracies):
    n = len(sampled_triples)
    mu_hat_wm = sum(accuracies[cluster] for cluster in sampled_triples) / n
    return mu_hat_wm

# Υπολογισμός του διαστήματος εμπιστοσύνης
def confidence_interval_twcs(sampled_triples, accuracies, mu_hat_wm, alpha=0.05):
    n = len(sampled_triples)
    if (n == 1):
        n=2
    variance = sum((accuracies[cluster] - mu_hat_wm) ** 2 for cluster in sampled_triples) / (n - 1)
    z = 1.96  # Για 95% CI
    ci_lower = mu_hat_wm - z * math.sqrt(variance / n)
    ci_upper = mu_hat_wm + z * math.sqrt(variance / n)
    return ci_lower, ci_upper


def main():
    # Φόρτωση των τριπλετών από το αρχείο
    triples = load_triples('output.txt')
    
    # Πρώτο στάδιο: Weighted Cluster Sampling (WCS)
    n = 4  # Αριθμός συστάδων στο δείγμα
    selected_clusters = weighted_cluster_sampling(triples, n)

    # Δεύτερο στάδιο: Επιλογή τριπλετών εντός των συστάδων (TWCS)
    m = 15  # Μέγιστος αριθμός τριπλετών ανά συστάδα
    sampled_triples = two_stage_sampling(triples, selected_clusters, m)

    # Εμφάνιση των επιλεγμένων συστάδων και τριπλετών
    print("Οι επιλεγμένες συστάδες και οι τριπλέτες που επιλέχθηκαν:")
    for cluster, triples in sampled_triples.items():
        print(f"Συστάδα: {cluster}")
        print("Τριπλέτες:")
        for triple in triples:
            print(triple)
        print() 

    # Εισαγωγή ακρίβειας για κάθε συστάδα που δειγματίστηκε
    accuracies = {}
    for cluster in sampled_triples:
        accuracy = float(input(f"Ποιο είναι το ποσοστό σωστών τριπλετών για τη συστάδα {cluster}; "))
        accuracies[cluster] = accuracy

    # Υπολογισμός του εκτιμητή Hansen-Hurwitz για TWCS
    mu_hat_wm = hansen_hurwitz_twcs_estimator(sampled_triples, accuracies)

    # Υπολογισμός του διαστήματος εμπιστοσύνης
    ci_lower, ci_upper = confidence_interval_twcs(sampled_triples, accuracies, mu_hat_wm)

    # Εμφάνιση αποτελεσμάτων
    print(f"Hansen-Hurwitz Estimator (TWCS): {mu_hat_wm}")
    print(f"Confidence Interval (TWCS): [{ci_lower}, {ci_upper}]")

if __name__ == "__main__":
    main()
