    rrr = np.random.random(size=(len(project_list))) * 1

    mm = {}
    for i, p in enumerate(project_list):
        mm[p['name']] = i

    project_list = sorted(project_list, key=lambda x: - x['score'] + 2 * x['duration'] + rrr[mm[x['name']]], reverse=False)
