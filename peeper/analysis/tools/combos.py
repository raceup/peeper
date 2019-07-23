def current_combo(rpms, torques):
    return [
        rpms[j] * 100 / 60 * 2 * 3.14159265354 * torques[j] / 350
        for j in range(len(rpms))
    ]
