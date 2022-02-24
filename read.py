with open('B.in', 'r') as in_file:
  line = in_file.readline()
  C = int(line.split()[0])
  P = int(line.split()[1])

  dev_skills = {}


  for i in range(C):
    line = in_file.readline()
    name = line.split()[0]    
    num_skills = int(line.split()[1])
    dev_skills[name] = []
    for j in range(num_skills):
      line = in_file.readline()
      lang = line.split()[0]
      level = int(line.split()[1])
      dev_skills[name].append((lang, level))


  projects = {}

  for i in range(P):
    line = in_file.readline().split()
    [name, D, S, B, R] = line
    projects[name] = {'days': int(D), 'score': int(S), 'best_before': int(B), 'roles': []}
    for j in range(int(R)):
      [lang, level] = in_file.readline().split()
      projects[name]['roles'].append((lang, int(level)))

  print(dev_skills)

  print(projects)
