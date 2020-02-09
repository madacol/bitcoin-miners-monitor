# Bitcoin miners monitor system
Python scripts that ran in a *Raspberry Pi* to monitor bitcoin miners (Antminer S5) through LAN

# Scripts tasks

- Gather following indicators through the **cgminer's HTTP API**:
  - HashRate
  - temperatures
  - active pool
  - chain asics health status
- Analyse and mailed any unusual activity using Linux's `exim4` mailer.
- Send data to **Google Forms**

### Data example:
    # timestamp, ip's last byte, temp1, temp2, hashrate, active pool, chain asics health status

    19/5/2015 22:34:44, 172, 51, 54, 1147.4, stratum tcp://stratum.f2pool.com:3333, ['oooooooo oooooooo oooooooo oooooo ', 'oooooooo oooooooo oooooooo oooooo ']

---

Graphing and analysis where made in **Google Sheets** feeded through the **Google Forms**