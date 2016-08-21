def feries(annee):
    '''
    On calcule les dates des jours fériés fixes ou
    variables selon les années (lundi de paques,
    lundi de pentecote et jeudi de l'ascension).
    '''

    # La plupart des jours feriés sont fixes
    feries = [
        '1/1',
        '1/5',
        '8/5',
        '14/7',
        '15/8',
        '1/11',
        '11/11',
        '25/12'
    ]

    # Lundi de Pâques
    a = annee // 100
    b = annee % 100
    c = (3 * (a + 25)) // 4
    d = (3 * (a + 25)) % 4
    e = (8 * (a + 11)) // 25
    f = (5 * a + b) % 19
    g = (19 * f + c - e) % 30
    h = (f + 11 * g) // 319
    j = (60 * (5 - d) + b) // 4
    k = (60 * (5 - d) + b) % 4
    m = (2 * j - k - g + h) % 7
    n2 = (g - h + m + 115) // 31
    p2 = (g - h + m + 115) % 31
    paques_jour = p2 + 1
    paques_mois = n2

    # Lundi de Pentecôte
    n3 = (g - h + m + 165) // 31
    p3 = (g - h + m + 165) % 31
    pentecote_jour = p3 + 1
    pentecote_mois = n3

    # Jeudi de l'Ascension
    n4 = (g - h + m + 154) // 31
    p4 = (g - h + m + 154) % 31
    ascension_jour = p4 + 1
    ascension_mois = n4

    # On ajoute les feriés variables aux feriés fixes
    feries += [
        '{0}/{1}'.format(paques_jour, paques_mois),
        '{0}/{1}'.format(pentecote_jour, pentecote_mois),
        '{0}/{1}'.format(ascension_jour, ascension_mois),
    ]

    return feries