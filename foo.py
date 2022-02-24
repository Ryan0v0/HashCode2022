dev_skills = {}
projects = {}

inputs = ['a_an_example.in.txt', 'b_better_start_small.in.txt', 'c_collaboration.in.txt',
  'd_dense_schedule.in.txt', 'e_exceptional_skills.in.txt']

with open(f'input_data/{inputs[4]}', 'r') as in_file:
  line = in_file.readline()
  C = int(line.split()[0])
  P = int(line.split()[1])


  for i in range(C):
    line = in_file.readline()
    name = line.split()[0]    
    num_skills = int(line.split()[1])

    lang_level = {}
    for j in range(num_skills):
      line = in_file.readline()
      lang = line.split()[0]
      level = int(line.split()[1])
      lang_level[lang] = level

    dev_skills[name] = lang_level


  for i in range(P):
    line = in_file.readline().split()
    [name, D, S, B, R] = line
    projects[name] = {'days': int(D), 'score': int(S), 'best_before': int(B), 'roles': []}
    for j in range(int(R)):
      [lang, level] = in_file.readline().split()
      projects[name]['roles'].append((lang, int(level)))

  # print(dev_skills)
  # print(projects)


with open('out.txt', 'w') as out_file:
  ans = []  
  proj_l = sorted(projects.items(), key = lambda t: t[1]['best_before'], reverse=False)
  # print(proj_l)

  for name, info in proj_l:
    assignee = []
    used = set()
    for (lang, lvl) in info['roles']:
      found = False
      for dev_name, skills in dev_skills.items():
        if lang in skills and skills[lang] >= lvl and not dev_name in used:
          assignee.append(dev_name)
          used.add(dev_name)
          found = True
          break
        if found:
          break


    if(len(assignee) == len(info['roles'])):
      ans.append((name, ' '.join(assignee)))


  out_file.write(f'{len(ans)}\n')
  for (name, res) in ans:
    out_file.write(f'{name}\n')
    out_file.write(f'{res}\n')

