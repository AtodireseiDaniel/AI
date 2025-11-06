import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

k = 180
T = 10

alpha_prior = 0.001
beta_prior = 0.001

lambda_values = np.linspace(0.001, 40, 5000)

prior_pdf = stats.gamma.pdf(
    lambda_values,
    a=alpha_prior,
    scale=1 / beta_prior
)




likelihood = stats.poisson.pmf(k, mu=T * lambda_values)

unnormalized_posterior = likelihood * prior_pdf
a = np.trapezoid(unnormalized_posterior, lambda_values)
posterior_pdf = unnormalized_posterior / (a)

mean_posterior = np.trapezoid(lambda_values * posterior_pdf, lambda_values)

mode_idx = np.argmax(posterior_pdf)
mode_posterior = lambda_values[mode_idx]


def shortest_hdi_from_grid(x_grid, pdf, cred_mass=0.94):
    dx = x_grid[1] - x_grid[0]
    cdf = np.cumsum(pdf) * dx
    n = len(x_grid)
    best_low, best_high = None, None
    best_width = np.inf

    cdf_max = cdf[-1]

    for i in range(n):
        target = cdf[i] + (cred_mass * cdf_max)

        if target > cdf_max:
            break

        j = np.searchsorted(cdf, target)

        if j < n:
            width = x_grid[j] - x_grid[i]
            if width < best_width:
                best_width = width
                best_low = x_grid[i]
                best_high = x_grid[j]

    if best_low is None:
        return x_grid[0], x_grid[-1]

    return best_low, best_high


hdi_low, hdi_high = shortest_hdi_from_grid(lambda_values, posterior_pdf, cred_mass=0.94)

alpha_post_analitic = alpha_prior + k
beta_post_analitic = beta_prior + T
mode_analitic = (alpha_post_analitic - 1) / beta_post_analitic


print(f"a) α'={alpha_post_analitic:.3f}, β'={beta_post_analitic:.3f})")
print(f"b)  [{hdi_low:.6f}, {hdi_high:.6f}]")
print(f"c)  {mode_analitic:.6f}")
print(f"   (Verificare Mod numeric: {mode_posterior:.6f})")


plt.figure(figsize=(12, 6))
plt.plot(lambda_values, posterior_pdf, label='Posterior (pe grilă)', color='blue')
plt.axvline(mean_posterior, color='red', linestyle='--', label=f'Media posterior = {mean_posterior:.2f}')
plt.axvline(mode_posterior, color='green', linestyle='--', label=f'Moda posterior = {mode_posterior:.2f}')
plt.fill_between(lambda_values, posterior_pdf, where=(lambda_values >= hdi_low) & (lambda_values <= hdi_high),
                 color='gray', alpha=0.4, label='94% HDI')
plt.xlim(10, 25)
plt.xlabel('λ (apeluri/oră)')
plt.ylabel('Densitate (aprox)')
plt.title('Posterior numeric pentru λ (prior: Gamma)')
plt.legend()
plt.grid(True)
plt.show()