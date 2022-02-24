# Map contributor name to skill level
contributors = []

# Map skills to contributors
skill_search = {}

# Projects
projects = []

with open('f_find_great_mentors.in.txt', 'r') as f:
    c, p = map(int, f.readline().split())
    for _ in range(c):
        name, skill_num = f.readline().split()
        contributor = {'name': name, 'skills': {}, 'available': True}
        skill_num = int(skill_num)
        for _ in range(skill_num):
            skill_name, skill_lvl = f.readline().split()
            skill_lvl = int(skill_lvl)
            contributor['skills'][skill_name] = skill_lvl
            skill_dict = {}
            if skill_name in skill_search:
                skill_dict = skill_search[skill_name]
            else:
                skill_search[skill_name] = skill_dict
            if skill_lvl in skill_dict:
                skill_dict[skill_lvl].append(contributor)
            else:
                skill_dict[skill_lvl] = [contributor]
        contributors.append(contributor)

    for _ in range(p):
        tokens = f.readline().split()
        name = tokens[0]
        duration, score, deadline, roles = map(int, tokens[1:])
        project = {
            "name": name, "roles": [], 'duration': duration,
            'score': score, 'deadline': deadline
        }
        for _ in range(roles):
            skill_name, skill_lvl = f.readline().split()
            skill_lvl = int(skill_lvl)
            project["roles"].append((skill_name, skill_lvl))
        projects.append(project)

    print(contributors)
    print(projects)
    print(skill_search)

def match_skill(skill_name, skill_req, has_mentor):
    skill_dict = skill_search[skill_name]
    max_lvl = max(skill_dict.keys())
    skill_lvl = skill_req - (1 if has_mentor else 0)
    while skill_lvl <= max_lvl:
        if skill_lvl in skill_dict:
            for contributor in sorted(skill_dict[skill_lvl], key=lambda x: sum(x['skills'].values())/len(x['skills'])):
                if contributor['available']:
                    if skill_lvl <= skill_req:
                        return contributor, True
                    else:
                        return contributor, False
        skill_lvl += 1
    return None, False

def rewind(update):
    for contributor, _ in update:
        contributor['available'] = True

def execute(update):
    for contributor, skill_name in update:
        if skill_name:
            skill_lvl = contributor['skills'][skill_name]
            skill_dict = skill_search[skill_name]
            contributor['skills'][skill_name] += 1
            skill_dict[skill_lvl].remove(contributor)
            skill_lvl += 1
            if skill_lvl in skill_dict:
                skill_dict[skill_lvl].append(contributor)
            else:
                skill_dict[skill_lvl] = [contributor]
        contributor['available'] = True

project_list = projects[:]
completed_projects = []
updates = {}
time = 0

while project_list:
    print(time)
    if time in updates:
        for update in updates[time]:
            execute(update)
        del(updates[time])
    project_list = sorted(project_list, key=lambda x: x['score'] / x['duration'], reverse=True)
    for project in project_list:
        if time + project['duration'] > project['deadline']:
            project['score'] -= 1
            if project['score'] == 0:
                project_list.remove(project)
            continue
        project['members'] = []
        update = []
        completable = True
        for skill_name, skill_lvl in project['roles']:
            has_mentor = False
            for member in project['members']:
                if skill_name in member['skills'] and member['skills'][skill_name] > skill_lvl:
                    has_mentor = True
                    break
            contributor, upgradable = match_skill(skill_name, skill_lvl, has_mentor)
            if contributor:
                project['members'].append(contributor)
                contributor['available'] = False
                update.append((contributor, skill_name if upgradable else None))
            else:
                completable = False
                break
        if completable:
            finish_time = time + project['duration']
            if finish_time in updates:
                updates[finish_time].append(update)
            else:
                updates[finish_time] = [update]
            completed_projects.append((project['name'], list(map(lambda m: m['name'], project['members']))))
            project_list.remove(project)
        else:
            rewind(update)
    if updates:
        time = min(updates.keys())
    else:
        break

print(completed_projects)

with open('f_out.txt', 'w') as f:
    f.write(f'{len(completed_projects)}\n')
    for project in completed_projects:
        f.write(f"{project[0]}\n{' '.join(project[1])}\n")







