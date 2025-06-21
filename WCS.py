import random
import math

# Load triplets from file
def load_triples(file_path):
    clusters = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Διαχωρισμός με βάση το κόμμα (και διαγραφή κενών που πιθανόν υπάρχουν)
            subject, predicate, obj = [x.strip() for x in line.strip().split(',')]
            if subject not in clusters:
                clusters[subject] = []
            clusters[subject].append((subject, predicate, obj))
    return clusters

# Υπολογίζουμε το μέγεθος κάθε συστάδας
def calculate_cluster_sizes(clusters):
    cluster_sizes = {cluster: len(triples) for cluster, triples in clusters.items()}
    total_size = sum(cluster_sizes.values())
    probabilities = {cluster: size / total_size for cluster, size in cluster_sizes.items()}
    return cluster_sizes, probabilities

# Επιλογή συστάδων με βάρη
def weighted_sampling(clusters, probabilities, n):
    return random.choices(list(clusters.keys()), weights=list(probabilities.values()), k=n)

# Υπολογισμός εκτιμητή Hansen-Hurwitz
def hansen_hurwitz_estimator(mu_values, n):
    return sum(mu_values) / n

# Υπολογισμός διαστήματος εμπιστοσύνης
def confidence_interval(mu_values, estimator, n, alpha=0.05):
    z_alpha_over_2 = 1.96  # Για 95% διάστημα εμπιστοσύνης
    variance = (1 / (n * (n - 1))) * sum((mu - estimator) ** 2 for mu in mu_values)
    margin_of_error = z_alpha_over_2 * math.sqrt(variance)
    return estimator - margin_of_error, estimator + margin_of_error


def main(file_path):
    clusters = load_triples(file_path)
    cluster_sizes, probabilities = calculate_cluster_sizes(clusters)
    
    # Επιλέγουμε 4 συστάδες με βάρη
    sampled_clusters = weighted_sampling(clusters, probabilities, 4)
    
    mu_values = []
    print(f"Selected clusters: {sampled_clusters}")
    
    # Ζητάμε το ποσοστό σωστών τριπλετών για κάθε συστάδα
    for cluster in sampled_clusters:
        mu_k = float(input(f"Enter the accuracy (mu) for cluster '{cluster}': "))
        mu_values.append(mu_k)
    
    # Υπολογισμός εκτιμητή
    estimator = hansen_hurwitz_estimator(mu_values, len(sampled_clusters))
    print(f"Hansen-Hurwitz Estimator: {estimator}")
    
    # Υπολογισμός διαστήματος εμπιστοσύνης
    lower_bound, upper_bound = confidence_interval(mu_values, estimator, len(sampled_clusters))
    print(f"Confidence Interval: [{lower_bound}, {upper_bound}]")

# Εκτέλεση προγράμματος με το αρχείο
file_path = 'output2.txt'  
main(file_path)
