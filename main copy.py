ARCHS = ['U-Net', 'PSPNet', 'FPN']

# Regímenes: fully‐supervised, weakly‐supervised y semi‐supervised
REGIMES = ['A-Full', 'B10','B25','B50','B75',   # fully y weak
           'C10','C25','C50','C75']             # semi (VT etiquetado + VT sin etiqueta + Ameli sin etiqueta)

# Ablations y enhancers definidos según tu plan
ABLATIONS = ['D1','D2','D3']      # (p.ej. sin consistency, sin confianza, sin augment fuerte)
ENHANCERS = ['E1','E2','E3','E4']  # (p.ej. Dice+BCE, CBAM, CutMix, filtro confianza)

for arch in ARCHS:
    # 1) Fully / Weak / Semi regímenes
    for regime in REGIMES:
        train_and_evaluate(architecture=arch,regime=regime,method='base')                # método base sin cambios extra)

    # 2) Seleccionar el mejor semi‐supervised para esta arquitectura
    best_semi = select_best_regime(arch,regimes=['C10','C25','C50','C75'],metric='Val_IoU')

    # 3) Ablations sobre el mejor régimen semi
    for ab in ABLATIONS:
        train_and_evaluate(architecture=arch,regime=best_semi,method='ablation',ablation=ab)

    # 4) Enhancers sobre ese mismo régimen semi
    for enhancer in ENHANCERS:
        train_and_evaluate(architecture=arch,regime=best_semi,method='enhancer',enhancer=enhancer)
