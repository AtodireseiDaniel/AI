import pytensor
pytensor.config.cxx = ""
pytensor.config.mode = "FAST_COMPILE"

import pymc as pm
import pandas as pd
import numpy as np
import arviz as az

def main():
    df = pd.read_csv("Prices.csv")

    y = df["Price"].values
    x1 = df["Speed"].values
    x2 = np.log(df["HardDrive"].values)

    x1_s = (x1 - x1.mean()) / x1.std()
    x2_s = (x2 - x2.mean()) / x2.std()

    with pm.Model() as model:
        alpha = pm.Normal("alpha", mu=0, sigma=100)
        beta1 = pm.Normal("beta1", mu=0, sigma=10)
        beta2 = pm.Normal("beta2", mu=0, sigma=10)
        sigma = pm.HalfNormal("sigma", sigma=50)

        mu = alpha + beta1 * x1_s + beta2 * x2_s
        y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y)

        idata = pm.sample(2000, tune=2000, target_accept=0.9, random_seed=42)

    hdi_beta1 = az.hdi(idata.posterior["beta1"], hdi_prob=0.95)
    hdi_beta2 = az.hdi(idata.posterior["beta2"], hdi_prob=0.95)

    print("beta1:", hdi_beta1)
    print("beta2:", hdi_beta2)


    new_x1 = 33
    new_x2 = 540

    new_x1_s = (new_x1 - x1.mean()) / x1.std()
    new_x2_s = (np.log(new_x2) - x2.mean()) / x2.std()

    alpha_s = idata.posterior["alpha"].values.flatten()
    beta1_s = idata.posterior["beta1"].values.flatten()
    beta2_s = idata.posterior["beta2"].values.flatten()

    mu_samples = alpha_s + beta1_s * new_x1_s + beta2_s * new_x2_s

    mu_hdi = az.hdi(mu_samples, hdi_prob=0.90)
    print("c", mu_hdi)
if __name__ == "__main__":
    main()
