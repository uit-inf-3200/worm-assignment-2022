

<!-- GENERATED README FILE. DO NOT EDIT.    -->
<!-- source in worm-assignment-text/        -->

# Mandatory Assignment 2: The Worm

UiT INF-3203, Spring 2022 \
Mike Murphy and Otto Anshus

**Due date: Wednesday May 04 at 14:15**

## Contents

-   [Worm Assignment Overview](#worm-assignment-overview)
    -   [Background: What is a Worm?](#background-what-is-a-worm)
    -   [The Worm Gate](#the-worm-gate)
-   [Assignment Requirements](#assignment-requirements)
    -   [Worm Operation](#worm-operation)
    -   [Worm Operating Requirements](#worm-operating-requirements)
    -   [Required Experiments](#required-experiments)
    -   [Delivery](#delivery)
    -   [Demo](#demo)
    -   [Have Fun!](#have-fun)
-   [References](#bibliography)

## Also in This Repository

- [`worm_gate/`](worm_gate/) --- Code for the worm gates
- [`python_zip_example/`](python_zip_example/) --- An example
    of how to package a Python project into a single executable
<!-- Note to maintainer: Don't forget to update course URLs -->

## Worm Assignment Overview

Your assignment will be to create a distributed program that stays alive
in the face of failures. This program will be in the form of a *worm*.

### Background: What is a Worm?

Computer worms are a self-replicating computer program, similar to a
computer virus. The distinction is that while a virus runs by writing
its code into a host program, changing its behavior, a worm is more
independent: it enters a system via the network, runs as its own
process, and propagates from there.

Worms are typically malware and are rarely thought of as useful.
However, the worm concept started as an early and influential experiment
in distributed computing.

Computer worms were first described in a 1982 paper by John F. Shoch and
Jon A. Hupp [\[1\]](#ref-shoch1982Worm) at the renowned Xerox Palo Alto
Research Center. In Shoch and Hupp’s conception, a worm is a group of
cooperating processes, called *segments*, that propagate copies of
themselves across a local network and then work together to perform some
useful function. By replicating and propagating, the worm as a whole can
stay alive even if some segments or network nodes fail. They
experimented with several uses for worms, including acting as an
uncrashable alarm clock, displaying a “cartoon of the day,” and running
network diagnostics.

In this assignment, you will be building what Shoch and Hupp called “the
existential worm,” a worm with no payload (no alarm clock or cartoon),
simply a worm for its own sake. Your worm will propagate to different
nodes in our compute cluster and cooperate to keep itself both alive and
under control.

### The Worm Gate

To propagate, a worm needs some way to enter a computer and start
running. A malicious worm takes advantage of security holes in operating
systems and applications to “worm” its way into a system and trick the
system into starting the segment program. In Shoch and Hupp’s case,
their benevolent worms were deliberately allowed into the system via
their lab’s network-boot infrastructure.

For this assignment, we will provide a deliberate security hole in the
form of an HTTP server that simply accepts code from the internet and
runs it. We call this spectacularly unsafe program the *worm gate*. Our
worm gate will have a simple HTTP API that allows you to upload an
executable to run and also to kill any processes that the gate has
started. See the worm gate’s README file for details.

You will run this worm gate code on different nodes on the cluster, and
write a worm that uses it to propagate.

## Assignment Requirements

You should continue to work in your groups from the presentations and
assignment 1.

Your hand-in will include source code and a report. You will also
participate in an informal demo session like with the assignments in
INF-3200 last semester.

### Worm Operation

You will start the provided worm gate server on multiple nodes in the
cluster, then you will run your worm via those worm gates. For a
refresher on the cluster and how to access it, see the [cluster
intro](https://uit.instructure.com/courses/24935/pages/intro-to-our-compute-cluster)
and [paper
access/VPN](https://uit.instructure.com/courses/24935/pages/paper-access-vpn)
documents on Canvas. Remember that you can run multiple worm gates per
node by varying the port numbers.

Your worm will use the worm-gate’s upload mechanism to spread from node
to node to grow to a target size. If your worm is not at its target
size, it must either grow or shrink to the target size.

The worm gate can and will kill your worm segments. The worm should
notice that a segment is down and launch a replacement. It is also
possible that a worm gate might stop cooperating and start refusing
requests to run worm code.

Having a well-behaved worm will require communication and coordination
between segments. You may use any coordination strategy you choose. You
are encouraged to use a known consensus algorithm such as
Paxos [\[2\]](#ref-lamport2001PaxosMadeSimple),
[\[3\]](#ref-vanRenesse2015PaxosModeratelyComplex) or
Raft [\[4\]](#ref-ongaro2014Raft) for coordination. However, a simpler
algorithm will be accepted as long as it still results in a well-behaved
worm.

Your worm is not required to implement any particular API (the demo will
use the worm gate’s API). However, you will of course need to create
some interface for controlling your worm, including querying its status,
setting its target size, and most importantly, telling it to shut down.

You may use pre-written libraries, but be mindful that your worm segment
and any libraries it uses must be bundled into a single executable to
get in through the worm gate. Also be aware that pre-written libraries
might not line up perfectly with how you want to use them. For example,
previous students have reported being drawn to the
[PySyncObj](https://github.com/bakwc/PySyncObj) library, only to find
its API awkward to use for this task.

### Worm Operating Requirements

Your worm must operate within the following constraints:

#### The worm must maintain a consistent target size

The required experiments and the demo session will involve killing
segments and watching your worm recover. The number of running worm
segments must stay close to the target. Some margin of error or delay is
allowed, but the worm must not grow out of control.

#### The worm must propagate via the provided worm gate

You may not use SSH to start the worm program, and you may not use the
cluster’s shared file system to copy the program code or to communicate.
Imagine that the worm gate is a zero-day exploit that you are taking
advantage of. All code must enter through the worm gate.

Be aware that this requires bundling your worm segment into a single
executable. In particular, if your worm segment is a Python script that
relies on libraries you installed with `pip --user`, then it will be
very likely to break during the demo due to missing libraries. To avoid
that stressful situation, see the `python_zip_example/` directory in the
hand-out code for an example of how to bundle an entire Python project
into a single binary.

You may find that a compiled language is a better fit for this project.

#### Worm state must be kept in RAM

The worm must not touch the disk.

#### The worm must shut down when ordered to do so

Your worm must be a well-behaved worm. Robert T. Morris may be a
professor at MIT now [\[5\]](#ref-morrisCsail) (and one of the coauthors
of the Chord paper [\[6\]](#ref-chord)), but he got in a lot of trouble
as a grad student in 1988 when a worm he created got out of control and
crippled the early
internet [\[7\]](#ref-morrisCase)–[\[9\]](#ref-orman2003MorrisWormFifteenYears).

### Required Experiments

You must perform the following experiments to examine the behavior of
your worm:

1.  **Time to grow from 1 to 𝑛 segments,** for 𝑛 = 2…20

    Your worm will naturally start as a single segment. It should then
    grow to its target size. You will record how long it takes to grow
    and stabilize from 1 to 2, then repeat from 1 to 3, from 1 to 4, and
    so on, until you are growing from 1 to 20.

    How you perform the timing and how you determine that the worm is
    stable is up to you.

    You are also encouraged to experiment with larger worms, but trials
    up to 20 are required.

2.  **Time for worm of size 𝑛 to recover from 𝑘 segments killed,**
    where 𝑛 ≥ 10 and for 𝑘 = 1 … 𝑛-1

    Start with a worm of size 𝑛 ≥ 10 and send a command to one of the
    worm gates to kill the segment it is hosting. The worm should notice
    the missing segment and grow back to its target size. You will
    record how long this recovery takes. Repeat this experiment,
    increasing the number of segments killed until you are killing all
    but one segment.

    You may choose to perform this experiment with a larger worm, but 10
    segments is the minimum starting size.

Your report should include plots with the results of each experiment, as
well as discussion of the results.

You should perform multiple trials (at least 3) for each independent
variable, and plot the data with error bars.

Note that fast times are not necessarily the goal here. You will not be
penalized for having a slow worm. The goal is to increase your insights
into quantitatively evaluating what you build.

### Delivery

Your delivery must include source code and report. You must also
participate in a demo session similar to the assignments last semester.

Source and report must be bundled together in a zip file or tarball and
uploaded to Canvas before the demo session. This means that the deadline
is during the day, before class, not midnight.

#### Source Code

Your source code must include a README file with instructions for
running the code on the cluster.

#### Report

Your report should be in the form of a scientific paper and should
include background on worms, a description of your solution, results of
your experiments, and relevant discussion.

-   Describe the design decisions you made and why you made them. How do
    your segments communicate? What coordination algorithms did you use?
    If you used a known algorithm, how did you build the worm around it?
    What libraries did you use? How did you incorporate them? etc.

-   Describe your experiment methodology. How did you time the trials?
    How did you deterimine the worm was stable? etc.

-   A typical report length for this assignment is 3–6 pages. If you are
    far outside of that range, consider what you are missing or what you
    can cut.

See the [how to write a
report](https://uit.instructure.com/courses/24935/pages/how-to-write-a-report)
document on Canvas for a refresher on report format.

### Demo

Like in INF-3200 last semester, you will be required to give an informal
demo where you briefly describe your solution and run your code on the
cluster. No slides are necessary, but be prepared to discuss your
solution and how it might differ from the solutions of other groups.
During the demo, Mike will be in control of the worm-gate servers that
will run your worm segment code, and they may include some surprises not
present in the code we hand out.

### Have Fun!

This assignment is deliberately open-ended. We provide the worm gate,
and the rest is up to you. That is the fun and the challenge of this
assignment.

If you have questions, talk to Mike.

# References

<div id="refs" class="references csl-bib-body">

<div id="ref-shoch1982Worm" class="csl-entry">

<span class="csl-left-margin">\[1\] </span><span
class="csl-right-inline">J. F. Shoch and J. A. Hupp, “The ‘worm’
programs—early experience with a distributed computation,” *Commun.
ACM*, vol. 25, no. 3, pp. 172–180, Mar. 1982, doi:
[10.1145/358453.358455](https://doi.org/10.1145/358453.358455).</span>

</div>

<div id="ref-lamport2001PaxosMadeSimple" class="csl-entry">

<span class="csl-left-margin">\[2\] </span><span
class="csl-right-inline">L. Lamport, “Paxos made simple,” pp. 51–58,
2001, \[Online\]. Available:
<https://www.microsoft.com/en-us/research/publication/paxos-made-simple/>.</span>

</div>

<div id="ref-vanRenesse2015PaxosModeratelyComplex" class="csl-entry">

<span class="csl-left-margin">\[3\] </span><span
class="csl-right-inline">R. Van Renesse and D. Altinbuken, “Paxos made
moderately complex,” *ACM Comput. Surv.*, vol. 47, no. 3, pp.
42:1–42:36, Feb. 2015, doi:
[10.1145/2673577](https://doi.org/10.1145/2673577).</span>

</div>

<div id="ref-ongaro2014Raft" class="csl-entry">

<span class="csl-left-margin">\[4\] </span><span
class="csl-right-inline">D. Ongaro and J. Ousterhout, “In search of an
understandable consensus algorithm,” in *2014 USENIX annual technical
conference (USENIX ATC 14)*, Jun. 2014, pp. 305–319, \[Online\].
Available:
<https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro>.</span>

</div>

<div id="ref-morrisCsail" class="csl-entry">

<span class="csl-left-margin">\[5\] </span><span
class="csl-right-inline">MIT CSAIL, “Robert Morris: Professor.” Oct. 30,
2017, Accessed: Mar. 04, 2020. \[Online\]. Available:
<https://www.csail.mit.edu/person/robert-morris>.</span>

</div>

<div id="ref-chord" class="csl-entry">

<span class="csl-left-margin">\[6\] </span><span
class="csl-right-inline">I. Stoica *et al.*, “Chord: A scalable
peer-to-peer lookup protocol for internet applications,” *IEEE/ACM
Transactions on Networking*, vol. 11, no. 1, pp. 17–32, 2003, doi:
[10.1109/TNET.2002.808407](https://doi.org/10.1109/TNET.2002.808407).</span>

</div>

<div id="ref-morrisCase" class="csl-entry">

<span class="csl-left-margin">\[7\] </span><span
class="csl-right-inline">United States Court of Appeals, Second Circuit,
“United States vs. Morris.” 1991, Accessed: Mar. 04, 2020. \[Online\].
Available:
<https://scholar.google.com/scholar_case?case=551386241451639668>.</span>

</div>

<div id="ref-markoff1993ComputerIntruder" class="csl-entry">

<span class="csl-left-margin">\[8\] </span><span
class="csl-right-inline">J. Markoff, “Computer intruder is put on
probation and fined $10,000,” *The New York Times*, May 1990, Accessed:
Mar. 04, 2020. \[Online\]. Available:
<https://www.nytimes.com/1990/05/05/us/computer-intruder-is-put-on-probation-and-fined-10000.html>.</span>

</div>

<div id="ref-orman2003MorrisWormFifteenYears" class="csl-entry">

<span class="csl-left-margin">\[9\] </span><span
class="csl-right-inline">H. Orman, “The Morris worm: A fifteen-year
perspective,” *IEEE Security Privacy*, vol. 1, no. 5, pp. 35–43, 2003,
doi:
[10.1109/MSECP.2003.1236233](https://doi.org/10.1109/MSECP.2003.1236233).</span>

</div>

</div>
