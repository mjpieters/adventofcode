import re


class Reindeer(object):
    def __init__(self, name, speed, travel_time, rest_time):
        self.name = name
        self.speed = speed
        self.travel_time = travel_time
        self.rest_time = rest_time
        self.reset()

    def __eq__(self, other):
        if not isinstance(other, Reindeer):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def distance_travelled(self, total_time):
        periods = total_time // (self.travel_time + self.rest_time)
        travelled = min(
            total_time - (self.travel_time + self.rest_time) * periods,
            self.travel_time) + periods * self.travel_time
        return self.speed * travelled

    def reset(self):
        self.distance = 0
        self.score = 0
        self.running = True
        self.duration = self.travel_time

    def tick(self):
        if self.running:
            self.distance += self.speed
        self.duration -= 1
        if self.duration == 0:
            self.running = not self.running
            self.duration = (
                self.travel_time if self.running else self.rest_time)


def run_race(reindeer, race_duration):
    furthest_distance = 0
    reindeer_in_lead = set()
    datapoints = {r.name: [] for r in reindeer}
    for second in range(race_duration):
        for racing_reindeer in reindeer:
            racing_reindeer.tick()
            if racing_reindeer.distance > furthest_distance:
                furthest_distance = racing_reindeer.distance
                reindeer_in_lead = {racing_reindeer}
            elif racing_reindeer.distance == furthest_distance:
                reindeer_in_lead.add(racing_reindeer)
        for leading_reindeer in reindeer_in_lead:
            leading_reindeer.score += 1
        for racing_reindeer in reindeer:
            datapoints[racing_reindeer.name].append((
                racing_reindeer.distance, racing_reindeer.score))
    return max(r.score for r in reindeer), datapoints


def read_file(fileobj):
    line_pattern = re.compile(
        r'(\w+) can fly (\d+) km/s for (\d+) seconds, '
        r'but then must rest for (\d+) seconds.')
    return [
        Reindeer(name, int(speed), int(tt), int(rt))
        for line in fileobj if line.strip()
        for name, speed, tt, rt in (line_pattern.search(line).groups(),)
    ]


def plot_race(datapoints, max_distance, max_score, filename):
    import matplotlib.pyplot as plt
    plt.ioff()

    colours = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#c49c94',
        '#f7b6d2', '#c7c7c7', '#bcbd22']

    fig, ax = plt.subplots(1, 1, figsize=(14, 12))

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # plt.xlim(0, max_score)
    # plt.ylim(0, max_distance)

    plt.xticks(range(0, 1000, 200), fontsize=14)
    plt.yticks(range(0, 3000, 500), fontsize=14)

    for colour, (reindeer, data) in zip(colours, datapoints.items()):
        plt.plot(
            [distance for distance, score in data],
            [score for distance, score in data],
            lw=2.5, color=colour)

        y_pos = data[-1][0] - 0.5  # at same height as score
        plt.text(max_distance, y_pos, reindeer, fontsize=14,
                 color=colour)

    plt.savefig(filename, bbox_inches='tight')


if __name__ == '__main__':
    import sys
    import os.path

    filename = sys.argv[-2]
    race_duration = int(sys.argv[-1])
    with open(filename) as inf:
        reindeer = read_file(inf)
    max_distance = max(r.distance_travelled(race_duration)
                       for r in reindeer)
    print('Part 1:', max_distance)
    max_score, datapoints = run_race(reindeer, race_duration)
    print('Part 2:', max_score)

    if '--graph' in sys.argv:
        dirname, basename = os.path.split(filename)
        output = os.path.join(dirname, os.path.splitext(basename)[0] + '.png')
        plot_race(datapoints, max_distance, max_score, output)
        print('Saved graph to', output)
