import matplotlib.pyplot as plt


def single_policy(rate: list, policy: list, iterations: int, removed, susceptible, path):
    """
    Using data from simulation plot a graph with a single x-axs
    :param path: path for figure to be saved
    :param rate: rate of policy at each interval
    :param policy: the policy
    :param iterations: number of iterations played
    :param removed: the set of results concerning removed nodes
    :param susceptible: the set of results concerning susceptible nodes
    """
    plt.clf()
    y1 = susceptible
    y2 = removed
    current_rate = get_rate(rate, policy)
    if len(current_rate) > 1:
        x = current_rate
        plt.xlabel(get_x_label(policy))
    else:
        x = list(range(1, iterations + 1))
        plt.xlabel('X - Iterations')
    plt.plot(x, y1, label="Susceptible")
    plt.plot(x, y2, label="Removed")
    plt.ylabel('Y - nodes')
    plt.title('Covid Simulation on Lockdown intervention ')
    plt.legend()
    plt.savefig(path, bbox_inches='tight')
    return plt.gcf()


def double_policy(rate: list, policy: list, iterations: int, removed, susceptible, path):
    """
       Using data from simulation plot a graph with a two-axis or pass to single-axis
       :param path: path for plot to be saved
       :param rate: rate of policy at each interval
       :param policy: the policy
       :param iterations: number of iterations played
       :param removed: the set of results concerning removed nodes
       :param susceptible: the set of results concerning susceptible nodes
    """
    plt.clf()
    y1 = susceptible
    y2 = removed
    rate_one = get_rate(rate, policy[0])
    rate_two = get_rate(rate, policy[1])
    if len(rate_one) > 1 and len(rate_two) > 1:
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax2 = plt.twiny(ax1)
        ax1.plot(rate_one, y1, label="Susceptible")
        ax2.plot(rate_two, y2, label="Removed")
        ax2.plot(rate_two, y1, label="Susceptible")
        ax1.set_xlabel(r'' + get_x_label(policy[0]))
        ax2.set_xlabel(r'' + get_x_label(policy[1]))
        ax1.set_ylabel('Y - Nodes')
        plt.ylabel('Y - Nodes')
        plt.title('Covid Simulation on Lockdown Intervention ')
        plt.legend()
        plt.savefig(path, bbox_inches='tight')
        return plt.gcf()
    elif len(rate_one) > 1:
        return single_policy(rate, policy[0], iterations, removed, susceptible, path)
    elif len(rate_two) > 1:
        return single_policy(rate, policy[1], iterations, removed, susceptible, path)
    elif len(rate_two) == 1 and len(rate_one) == 1:
        return single_policy(rate, policy[0], iterations, removed, susceptible, path)


def triple_policy(rate: list, policy: list, iterations: int, removed, susceptible, path):
    """
       Using data from simulation decide which two axis to plot when three are present
       :param path: path for file to be saved
       :param rate: rate of policy at each interval
       :param policy: the policy
       :param iterations: number of iterations played
       :param removed: the set of results concerning removed nodes
       :param susceptible: the set of results concerning susceptible nodes
    """
    count = 0
    positions = []
    for i in range(0, len(policy)):
        if len(get_rate(rate, policy[i])) > 1:
            count += 1
            positions.append(i)
    if count == 0:
        return single_policy(rate, policy[0], iterations, removed, susceptible, path)
    if count == 1:
        return single_policy(rate, policy[positions[0]], iterations, removed, susceptible, path)
    else:
        new_policy_list = [policy[positions[0]], policy[positions[1]]]
        return double_policy(rate, new_policy_list, iterations, removed, susceptible, path)


def build(rate: list, policy: list, iterations, removed, susceptible, path):
    """

    :param path:
    :param rate:
    :param policy:
    :param iterations:
    :param removed:
    :param susceptible:
    :return:
    """
    size = len(policy)
    if size == 1:
        return single_policy(rate, policy[0], iterations, removed, susceptible, path)
    if size == 2:
        return double_policy(rate, policy, iterations, removed, susceptible, path)
    else:
        return triple_policy(rate, policy, iterations, removed, susceptible, path)


def get_rate(rate: list, policy: str):
    """
    Using policy name return the appropriate rate
    :param rate: the set of rates for each policy
    :param policy: the policy being returned
    :return: The rate sublist for the policy
    """
    if policy == "R":
        return rate[0]
    if policy == "Case":
        return rate[1]
    if policy == "Variance":
        return rate[2]
    if policy == "Cluster":
        return rate[3]
    if policy == "Isolation":
        return rate[4]
    if policy == "Tracing":
        return rate[5]


def get_x_label(policy):
    """
    Using the policy name return a suitable X-axis
    :param policy:
    :return: a string X-axis label
    """
    if policy == "R":
        return "X - R Rate"
    if policy == "Case":
        return "X - Daily Cases (%)"
    if policy == "Variance":
        return "X - Distribution Mean (Varied Individual Obedience)"
    if policy == "Cluster":
        return "X - Distribution Mean (Cluster Obedience)"
    if policy == "Isolation":
        return "X - Percentage of confirmed cases (Isolation)"
    if policy == "Tracing":
        return "X - Percentage of contacts traced from a confirmed case "

