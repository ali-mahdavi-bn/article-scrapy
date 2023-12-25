
## Ken: Kernel Extensions Using Natural Language

Yusheng Zheng eunomia-bpf Community Shanghai, Shanghai, China yunwei356@gmail.com Maolin Chen eunomia-bpf Community Shanghai, Shanghai, China agaaain.try@gmail.com Abstract The ability to modify and extend an operating system is an important feature for improving a system's security, reliability, and performance. The extended Berkeley Packet Filters
(eBPF) ecosystem has emerged as the standard mechanism for extending the Linux kernel and has recently been ported to Windows. eBPF programs inject new logic into the kernel that the system will execute before or after existing logic.

While the eBPF ecosystem provides a flexibility mechanism for kernel extension, it is difficult for developers to write eBPF programs today. An eBPF developer must have deep knowledge of the internals of the operating system to determine where to place logic and cope with programming limitations on the control flow and data accesses of their eBPF program enforced by the eBPF verifier. In the end, the limitations enforced by today's eBPF framework ensure that only expert kernel developers can extend their kernels.

This paper presents KEN, an alternative framework that alleviates the difficulty of writing an eBPF program by allowing Kernel Extensions to be written in Natural language. KEN uses recent advances in large language models (LLMs) to synthesize an eBPF program given a user's English language prompt. To ensure that LLM's output is semantically equivalent to the user's prompt, KEN employs a combination of LLM-empowered program comprehension, symbolic execution, and a series of feedback loops. KEN's key novelty is the combination of these techniques. In particular, the system uses symbolic execution in a novel structure that allows it to combine the results of program synthesis and program comprehension and build on the recent success that LLMs have shown for each of these tasks individually.

To evaluate KEN, we develop a new corpus of natural language prompts to eBPF programs. We show that KEN produces correct eBPF programs on 80%—which is an improvement of a factor of 2.67 compared to a LLM-empowered program synthesis baseline. Moreover, we find that KEN very rarely synthesizes "false positive" eBPF programs—i.e., eBPF programs that KEN verifies as correct but manual inspection reveals to be semantically incorrect for the input prompt. The code for KEN is publicly accessible at https://github.com/eunomiabpf/KEN.

Yiwei Yang UC Santa Cruz Santa Cruz, California, USA
yyang363@ucsc.edu Andrew Quinn UC Santa Cruz Santa Cruz, California, USA
aquinn@ucsc.edu
1
Introduction Developers are increasingly tasked with modifying and extending operating system kernels to improve performance, security, reliability, or introduce new features to their systems. Extended Berkeley Packet Filters (eBPF) have emerged as the de facto method for extending an operating system, with recent support for both Linux and Windows [19]. eBPF
programs inject new logic that is executed before or after existing kernel logic to observe or modify the kernel's behavior. eBPF programs were originally used to trace network traffic, but the ecosystem now provides sufficient power to implement a variety of features including performance monitoring performance [25, 27], detecting intrusion detection [5, 35], and application-specific logic [23, 37, 65, 66].

Unfortunately, eBPF programs are difficult to write correctly. Implementing an eBPF program requires intimate knowledge of kernel internals to identify where to inject logic [17]. Additionally, the eBPF verifier, intended to prevent unsafe eBPF programs from executing on a system, imposes a number of unfortunate programming constraints on eBPF programmers: programs can only use limited control flow (e.g., loops must have constant bounds) and limited data accesses (e.g., the program cannot access arbitrary memory). Consequently, eBPF is not even a Turing Complete language [41].

In this paper, we present KEN, a system that alleviates the difficulty of eBPF by allowing Kernel Extensions written in Natural language. KEN uses recent advances in large language models (LLMs) (e.g., OpenAI's InstructGPT[43], HumanEval[11], and *ChatGPT*[55]) to synthesis an eBPF
program given a user's English language prompt. A user can then extend their kernel by injecting the eBPF program produced by KEN without having to understand eBPF or a kernel's internals.

Alas, naively extending a kernel using the output from an LLM is dangerous. LLMs generate responses that can be unsafe or semantically incorrect. While the eBPF verifier prevents many unsafe eBPF programs from compromising the kernel, there are fundamental safety issues that remain unpatched [36]. Additionally, no existing tools provide assurances that the semantics of KEN's output eBPF program are equivalent to the semantics of the English language prompt input. Consequently, a naive LLM-based eBPF program synthesis tool only produces a correct program on 30% of programs for a representative set of kernel extension prompts.

KEN addresses the semantic correctness challenge by combining three techniques: automated program comprehension, symbolic execution, and feedback-loops. In addition to using an LLM in its *Synthesis Engine* to synthesize an eBPF
program for a user prompt, KEN also uses an LLM in its Comprehension Engine to identify Hoare-logic constraint that specifies the conditions that must hold before and after all kernel functions with which an eBPF candidate program interacts. KEN annotates its synthesized eBPF program with the constraints and passes the results to a symbolic execution engine to validate that the constraints are upheld by the eBPF program. If a candidate eBPF program passes the symbolic execution engine, KEN further validate its safety using the current eBPF verifier. KEN includes feedback loops to retry synthesis when the system fails to synthesize a verified eBPF program. It passes error messages back to reprompt itself on failure, which can happen because of a symbolic execution timeout, constraint failure during symbolic execution, or when the eBPF verifier fails.

KEN adopts state-of-the-art techniques for eBPF program synthesis throughout each of its key components (LLM- based program synthesis, LLM-based program comprehension, symbolic execution, and feedback loops). The system's key novelty lies in its synergistic combination of these techniques. In particular, KEN's use of symbolic execution is a novel structure that allows it to combine the results of program synthesis and program comprehension and build on the success that LLMs have shown for each task individually.

In addition to the system artifact, we produce two novel datasets as a part of this paper. These datasets are not only useful for building and evaluating KEN, but will also be useful for future work on eBPF program synthesis. First, eBPFNLDataset is a dataset of eBPF programs and natural language descriptions. eBPFNLDataset consists of 145 pairs of natural language prompts with eBPF programs. 65 of the paris are from a popular eBPF programming blog [24], while the remaining 80 are handwritten based upon examples from popular open-source eBPF repositories [4, 16, 48, 59]. Second, we created KernelCompDataset, a dataset of Hoare-logic contracts for all Linux functions that can be hooked by an eBPF program. We present a novel methodology for automatically generating such contracts by using the kernel's source code, developer comments embedded in the source code, and an LLM.

We validate KEN on eBPFNLDataset, using test programs from the blog as a training set and the new tests as the test set. We find that KEN produces semantically correct eBPF programs on 80%of the test cases, which is 2.67 times better than a naive strategy that only uses LLM-based program synthesis. Moreover, we find that KEN only produces a single "false positive"—an output program that passes KEN's verification but is not semantically correct for the provided prompt. In addition to these high-level results, we show that each of KEN's design principles—feedback-loops, LLM-
empowered program comprehension, symbolic execution, and training on the new eBPFNLDataset dataset—contributes to its strong results. Finally, we explore the performancecost-privacy tradeoffs between using large cloud-based LLMs
(e.g., ChatGPT-4 [55]) and small locally-deployable LLMs (e.g., CodeLLama) and show that the large cloud-based LLMs outperform the small LLMs by a factor of 5.3.

In summary, our contributions are:

- We present KEN, the first tool for safely expressing
operating system extensions in natural language using program synthesis, program comprehension, symbolic
execution, and feedback loops.
- We create two datasets: eBPFNLDataset, which provides a rich dataset of eBPF programs and natural language descriptions to aid with training and evaluating program synthesis for eBPF programs, and Kernel- CompDataset, which provides hoare-logic contracts for Linux helper functions to aid tune program comprehension.
- We evaluate KEN on eBPFNLDataset and show that
KEN accurately synthesizes eBPF programs on 80% of prompts in a representative test set while only verifying a semantically incorrect program in 2.5% of cases.
The rest of this paper proceeds as follows: First, we describe background on each of the techniques employed by KEN (section 2); then, we discuss KEN's design (section 3); next, we describe a case study as an example of how KEN
works (section 4); we describe our evaluation (section 5), elaborate on related work (section 6), and concluding (section 7).

## 2 Background This Section Describes Background On The Key Techniques That Ken Employs And A Discussion Of Common Ebpf Tasks. 2.1 Key Ken Techniques

We describe background for each of the key techniques upon which KEN builds.

2.1.1
Large Language Models. LLMs use machine learning to create sophisticated chat-like programs capable of creating useful responses to natural language prompts. Systems such as InstructGPT[43], *HumanEval*[11], and *ChatGPT* have employed LLMs for program synthesis, in which a developer prompts the systme with a natural language description of the program and the LLM responds with source code. Below we describe two standard techniques that have emerged for taking advantage of LLMs.

In-Context Learning. Systems that employ in-context Learning [9, 30, 39] adapt an LLM to a new target area by adding minimal contextual data to an LLM (e.g., they prompt the LLM with a small corpus of particularly pertinent inputs)
and carefully crafted prompts rather than training a custom LLM on a large dataset. In-context learning is more costeffective and can new data more quickly than traditional alternatives. The key challenges in employing in-context learning in a new synthesis domain involve identifying a corpus of critical examples and crafting a prompt strategy that guides the underlying LLM [9, 47].

Feedback Loops. Many systems employ a feedback-driven approach to validate an LLM's output against some specification and pass feedback to the model to refine the output. For example, HarmonyOS developers [62], Self-Debugging [12], and TPUv4 designers [51] use unit tests to evaluate whether an LLM's output is correct. The fundamental challenge in developing such ground truth unit tests—manually crafting a set of unit tests that can sufficiently guide the LLM is likely as difficult as manually writing the ideal synthesized output. Developers in the aforementioned examples were able to use unit tests that were already created for their use cases. Additionally, Self-Debugging includes a mechanism to provide feedback by using an LLM to explain the behavior of synthesized programs. The system refines its output by iteratively synthesizing programs, explaining the synthesized program and checking its unit-test outputs, and then iteratively re-synthesizing.

2.1.2
Automated Program Comprehension. Automated program comprehension determines properties of a program's execution without requiring developer effort. Early work [44] uses a counter-example driven approach, which observe a program under test and derive invariants that hold over all executions. Recent works shows that LLMs are effective at program comprehension tasks [1, 20, 21, 45, 63, 67], but their output is typically an English description of the program.

2.1.3
Symbolic Execution. Automated program verification has emerged to ensure that programs are correct without requiring a developer to write a copious amount of tests.

There are a wide range of existing solutions including model checking [15, 49], fuzzing [22], and symbolic execution (symbex) [8, 29]. KEN uses symbex because symbolic execution has been shown to be highly effective in finding issues both in operating systems [14] and user-programs [8, 29].

A symbolic execution engine reasons about the behavior of a function or program to determine whether the program upholds specific properties (e.g., memory safety). A symbex engine associates a symbolic value with each variable in the program. As the program executes, the engine gathers constraints on the symbolic values (e.g., variable x is less than 3). During execution, the engine uses an SMT solver Prompt 1: If a process tries to use ptrace, it should be killed with signal 2 and its PID should be displayed.

Prompt 2: Capture and display all bash commands executed system-wide, along with their exit codes.

Prompt 3: If the fan speed is within 90% of its maximum limit, modify the scheduling policy to optimize performance.

Figure 1. Descriptions of typical eBPF management/observability programs. to determine if a given property (e.g., "can this pointer be equal to NULL?") can be violated given the constraints that the engine gathered. Thus, symbolic execution can reason about large classes of inputs to a function or program without needing to execute each input individually. Symbolic Execution Engines face two fundamental challenges: Path Explosion and Verification Properties.

Path Explosion. The number of control-flow paths through a program is exponential in the number of conditional operations in the program. To ensure full coverage of a program, a symbolic execution engines must consider each of these exponentially many paths; this challenge is known as "the path explosion problem". One main consequence of the path explosion problem is that symbolic execution is traditionally limited to analyzing relatively small programs and/or individual functions within programs.

Verification Properties. Most symbolic execution engines verify that programs satisfy high-level properties such as memory safety (e.g., the program does not dereference a NULL pointer) and safe arithmetic (e.g., the program does not divide by zero). Some systems have used symbex to ensure that each function satisfies Hoare-logic-style pre- and post-conditions of individual functions [13, 46].

## 2.2 Ebpf: Extended Berkeley Packet Filter

Operating system extension is a critical task for developers today. Numerous techniques have been developed to ensure safe kernel extensions [7, 42, 54], with extended Berkeley Packet Filters (eBPF) recently emerging as the de facto standard for today's systems. eBPF permits custom user-defined program execution within the kernel space without the need to alter the kernel's source or load additional modules. To preserve system security, the eBPF verifier[57] verifies security critical properties of eBPF code prior to its execution. Figure 1 includes three examples of management and observability programs that can be written using eBPF. In addition to such management tasks, eBPF has been used for scheduling [31, 56], security [34], and custom file system rules [66]. For example, Google's Pixel6 kernel [56] uses eBPF to implement a power-aware real-time scheduler that applies handwritten rules to optimize CPU performance based on user
1
#!/usr/bin/env bpftrace
2 3
tracepoint:syscalls:sys_enter_kill
4
{
5
@tpid[tid] = args.pid;
6
@tsig[tid] = args.sig;
7
}
8
tracepoint:syscalls:sys_exit_kill
9
/@tpid[tid]/
10
{
11
time("%H:%M:%S
");
12
printf("**%-6d %-16s %-4d %-6d %d**\n", pid, comm, @tsig[tid], @tpid[tid],
13
args.ret);
14
delete(@tpid[tid]);
15
delete(@tsig[tid]);
16
}
activity. In one case, the Pixel6 kernel includes an eBPF program that reduces the CPU frequency immediately after a user closes a game.

The eBPF ecosystem includes multiple frameworks for building tools—the two dominate approaches being bpftrace and libbpf. libbpf is a C/C++ library that offers a numerous helper functions and structures to use when extending the kernel. In contrast, bpftrace provides a high-level scripting interface; fig. 2 provides an example bpftrace script for Prompt 2 in fig. 1 . can compile bpftrace programs into injectable eBPF bytecode by using the BCC library. Conventional wisdom is that libbpf implementations are more flexible than bpftrace implementations (i.e., a developer can implement more tasks), but also have more programming complexity [26]. Writing an eBPF program for either framework can be daunting, since a developer needs to understand operating system internals to determine where to inject logic, and is limited in the control flow and data accesses that they can issue.

3
System Design This section describes the design and implementation of KEN; Figure 3 depicts the system's key components and how they interact. KEN consists of four main components: a Prompter (section 3.2), responsible for constructing prompts that generate eBPF programs; a Synthesis Engine (section 3.3), responsible for synthesizing a candidate eBPF program given a natural language prompt; a Comprehension Engine (section 3.4), responsible for annotating a candidate eBPF program with accurate Hoare-logic conditions for each of the kernel functions with which the candidate interacts; and the Symbolic Verifier (section 3.5), responsible for ensuring that the candidate eBPF program upholds the Hoare-logic annotations. The system also uses the existing eBPF verifier to ensure that the eBPF candidate meets basic security criteria.

KEN uses in-context learning (section 2.1.1) to augment existing LLMs without requiring training of an entirely new model. This design allows KEN to remain LLM agnostic— the system can use any LLM and thus supports a variety of cost-performance-privacy tradeoffs (section 5.3). Supporting in-context learning requires two technical contributions: prompting strategies that guide the LLMs to produce correct output and new datasets for the Synthesis and Comprehension Engines.

KEN uses a feedback-driven approach to iteratively synthesize a correct eBPF program. KEN includes two such feedback loops. First, if the Symbolic Verifier determines that a candidate eBPF program from the Synthesis Engine does not uphold the Hoare-logic conditions from the Comprehension Engine or if the Symbolic Verifier times out, then the Verifier will pass the failure back to the Prompter. This feedback loop allows both Engines additional chances to synthesize correct output. The second feedback is from the eBPF verifier to the Prompter and is taken when the eBPF verifier does not verify that the synthesized eBPF program is safe.

Each of KEN's components is an adoption of state-of-theart techniques to the problem of eBPF program synthesis. KEN's key novelty lies in its combination of these techniques which empowers a useful and efficient program synthesis tool. In particular, KEN's use of symbolic execution to combine the results of program synthesis and program comprehension is a novel structure that allows KEN to build on the power that LLMs have shown on both tasks individually.

The rest of this section proceeds as follows. We first describe the workflow of synthesizing an eBPF program for a user prompt (section 3.1). Then, we discuss each of KEN's components (section 3.2–section 3.6). Finally, we describe KEN's implementation details (section 3.7).

## 3.1 Workflow

The high-level workflow for synthesizing an eBPF program in KEN is as follows. The user issues a prompt to the Prompter, which forwards the user's prompt to KEN's Synthesis Engine.

The Synthesis Engine consults an LLM to synthesize a candidate eBPF program based upon the user's input. KEN passes the candidate eBPF program to the Comprehension Engine, which consults an LLM to annotate the candidate eBPF program with Hoare-logic pre- and post-conditions for each of the Kernel functions that is referenced in the candidate eBPF program. KEN passes this annotated eBPF candidate to its Symbolic Verifier, which validates that the synthesized eBPF program satisfies the Hoare-logic properties. If the Symbolic Verifier determines that the eBPF program does not uphold the semantic properties, or if the Symbolic Verifier times out, then the Symbolic Verifier passes its output to the Prompter to begin another iteration of KEN. If the Symbolic Verifier succeeds, it passes the eBPF program to the eBPF verifier to validate the program's safety properties. The eBPF verifier will pass its error message to the Prompter to begin another iteration of KEN if the eBPF program is deemed unsafe.

If KEN fails to synthesize a verified eBPF program after a configured number of trials (3 is the default), the system will re-prompt the user to include additional information. Anecdotally, we observe that including small additional semantic hints (e.g., hinting at the expected size of some variables) can often resolve KEN's synthesis issues.

3.2
Prompter The Prompter takes the input prompt from the user and specially formats it to pass to the synthesis engine. In particular, the Prompter adds boilerplate text instructing KEN to produce an eBPF program written for bpftrace framework 1.

Additionally, the Prompter appends all error messages that it has received for the current synthesis task by all feedback loops. For example, if the Symbolic Verifier failed in a first iteration with message failure1 and the eBPF verifier failed in a second iteration with message failure2, then the Prompter will append both failure1 and failure2 to its message before sending it to the Synthesis Engine.

3.3
Synthesis Engine The Synthesis Engine takes a natural language prompt and consults an LLM to generate a candidate eBPF program. The engine uses LangChain [32] as mechanism for interacting with an arbitrary LLM, which allows KEN to support a variety of privacy-cost-performance tradeoffs.

Like other systems [12], the Synthesis Engine uses a VectorDB (e.g., Milvus [60]) to enable in-context learning. The engine stores prompt-eBPF pairs from the eBPFNLDataset dataset (see below) in its vectorDB. On each query, the engine uses the VectorDB to identify the prompt-eBPF pairs that are most similar to the user prompt and includes these pairs as examples of correct input-output pairs in its query to the large language model. Thus, KEN is similar to few-shot learning [61]. KEN also updates its VectorDB after each synthesis, which allows the system to learn from its successful and failure eBPF syntheses.

By specifying the desired syntax in the LLM prompt, we find that the Synthesis Engine almost always synthesizes correct syntax. Our results show that it also often synthesizes correct semantics (section 5).

eBPFNLDataset—an eBPF synthesis Dataset. The Synthesis Engine is empowered by eBPFNLDataset, a novel dataset of 145 natural language prompts paired with corresponding eBPF programs, 79 of which are bpftrace programs and 66 of which are libbpf programs. eBPFNLDataset was gathered from two sources. First, 65 pairs (39 bpftrace, 26 libbpf) come from a popular eBPF developer blog [24]. The other 80 pairs (40 bpftrace, 40 libbpf) are hardwritten based upon examples from well-known open-source eBPF project repositories, such as bcc[48], bpftrace[59], ebpf-exporter[16], or eunomia-bpf[4]. One example pair is Prompt 2 from fig. 1 and the bpftrace script from fig. 2.

3.4
Comprehension Engine The Comprehension Engines takes an eBPF candidate program as input and annotates it with Hoare-logic pre- and post- conditions at the beginning and end of each of the synthesized eBPF functions. The engine first uses a regular expression to identify the kernel locations that the candidate program instruments. The Comprehension Engine obtains the pre- and post-conditions for each kernel location by consulting the KernelCompDataset, which includes pre- and post-conditions that hold for each function that can be instrumented by eBPF (see below).

The Comprehension Engine prompts an LLM using LangChain.

Its prompt asks the LLM to create assert or assume statements for the beginning and end of each function in the eBPF program, respectively. The prompt includes the eBPF function, the original developer prompt, and together with the pre- and post-conditions obtained from the KernelCompDataset. The engine produces output that annotates the candidate eBPF program with LLM-generated assert/assume statements. Note that KEN could directly use the pre-/postconditions from the KernelCompDataset to construct assume and assert statements. However, its output would not be able to use the developer's prompt when generating assume/assert statements and would produce fewer semantically correct programs. Moreover, passing the pre-/postconditions through the LLM allows KEN to smooth out any inaccuracies in the KernelCompDataset—which arise because the KernelCompDataset is automatically generated and thus neither sound nor complete. Finally, using an LLM allows the Comprehension Engine to learn from its mistakes and successes, like the Synthesis Engine, by updating an internal VectorDB on every prompt.

It is worth noting that the LLM in a Comprehension Engine could nefariously adjust its pre-/post-conditions so that all candidate eBPF programs are tautologically verified by the symbolic verifier. Our evaluation (section 5) shows empirically that this is not the case since KEN synthesizes few
"false positives"—i.e., programs that the system verifies but that manual inspect reveals to not implement the same semantics as the natural language prompt. We hypothesize that one reason that we do not see the Comprehension Engine gaming the system towards tautology is that the engine's VectorDB learns slowly and so we do not observe the VectorDB drastically impacting the LLM behavior. It is possible that a extremely long-running deployment would observe more such false positives. This issue could then be resolved by occasionally clearing the Comprehensive Engine's VectorDB.

KernelCompDataset—a dataset of Hoare-logic contracts for kernel functions. Manually creating a dataset of Hoare-logic contracts for every eBPF instrumentable kernel function would be infeasible. There are hundreds of such functions, and the functions themselves change with each new kernel release. Thus, we chose to generate KernelCompDataset using an automated approach that we can then adapt to new kernel versions. We use a regular expression to identify every function that has a symbol in the kernel.

To approximate the function's semantics, we use a regular expression to find any comments immediately before the function. We pass the function prototype, source code, and approximate semantics into an LLM using a prompt that asks for Z3 compatible conditions for each of the eBPF helpers. We store the approximate semantics, prototype, and the output from the LLM in a JSON format in the KernelCompDataset. If detected, developers could fix inaccuracies from the automated approach, although we have not needed to do so in KEN.

3.5
Symbolic Verifier The symbolic verifier uses symbolic execution to validate the annotated eBPF candidate program produced the Comprehension Engine. If the symbolic verifier determines that the program upholds the assert statements, it removes the assert/assume statements and passes the candidate eBPF program to the eBPF verifier. If the symbolic verifier finds an assertion statement that is not upheld or times out, then it passes its error message to the Prompter.

## 3.6 Ebpf Verifier

KEN uses the existing eBPF Verifier from the operating system. Namely, the eBPF Verifier validates that the eBPF candidate program produced by the Symbolic Verifier contains no unbounded loops or arbitrary memory accesses. If the eBPF
verifier is unable to assure that the candidate program is safe, it passes its error message back to the Prompter. Otherwise, the eBPF verifier passes the eBPF candidate program to the user as its final synthesized eBPF program.

## 3.7 Implementation

We implement KEN, eBPFNLDataset, and KernelCompDataset using 4244 LOC in Python and 490 LOC cumulatively acrosss HTML, CSS, and JS. In addition, we add 51 LOC to the bpftrace compiler to add support for assume and assert functions. KEN uses SeaHorn [29] as its Symbolic Verifier and Z3 [18] as its backend SMT solver. SeaHorn symbolically executes LLMV IR; KEN uses SeaHorn by compiling the output of the Comprehension Engine to LLVM IR.

KEN supports a multitude of LLM, but employs ChatGPT-
4 by default. While eBPF is now supported in Windows, our current KEN prototype only works on Linux. KEN can synthesize eBPF programs for both libbpf and bpftrace, but it defaults to bpftrace because we found that KEN is more effective at synthesizing bpftrace programs (section 5).

## 4 Case Study

This section describes a case study of using KEN to provide an example of how each of KEN's steps work. We crafted this scenario specifically to illustrate KEN's behavior; it is not a test from eBPFNLDataset.

In this case study, a user wishes to display information to their terminal about all of the tcp connections that are made to their webserver so that they can detect denial of service attacks that are made against it. Kernel extensions offers a good mechanism for performing full system telemetry. However, since the developer is not a linux kernel expert, they turn to KEN to help them build their eBPF program. Figure 4 shows the developer's prompt that the developer issues to KEN. They ask the system to trace all IPv4 and IPv6 tcp_connect events and specify their desired output including the proper order for each port.

KEN Prompter passes the user's prompt to the Synthesis Engine, which generates the output program shown in fig. 5. The program parses the relevant data from the sk parameter of the kernel probe tcp_connect. The Synthesis Engine passes the synthesized candidate eBPF program to the Comprehension Engine.

Prompt: Write a bpftrace program to trace tcp_connect events for both IPv4 and IPv6 connection attempts, display the source and destination IP
addresses and the source and destination ports in host byte order.

$saddr = ntop(2, $sk->__sk_common.skc_rcv_saddr);
$daddr = ntop(2, $sk->__sk_common.skc_daddr);
$sport = ($sk->__sk_common.skc_num);
$dport = ($sk->__sk_common.skc_dport);
printf("TCP connect: %s:%d -> %s:%d\n", $saddr, $sport,

    $daddr, $dport);
↩→

}

"kretprobe:tcp_connect_init": {
"pre": {
"sk": "!=null",
}
}
The Comprehension Engine first uses a regular expression to lookup any pre- and post-conditions in its KernelComp- Dataset for the tcp_connect kprobe. Figure 6 shows the matching pre-condition. The Comprehension Engine then prompts its LLM to identify assert and assume statements for the candidate eBPF program, passing input as the matching pre-condition, the original user prompt, and the candidate eBPF program. Figure 7 shows the annotated eBPF candidate program generated by adding the LLM generated assume and assert statements. The LLM generates the assume in pink based upon the pre-condition from the KernelCompDataset element. The LLM generates the yellow assume statements based upon the user prompt. Finally, the LLM generates the assert statements in blue based upon the users prompt. Note that the final statement determines that bytes should be swapped because the user's query asks for host byte order.

Then, KEN passes the annotated eBPF candidate program to the symbolic verification engine. The engine translates the assume an assert statements into SMT formulas and passes them to Z3 to verify if the originally generated eBPF program satisfies both the safety requirements from the eBPF verifier and semantics requirements from the prompt. Specifically,
$sport = ($sk->__sk_common.skc_num); $dport = ($sk->__sk_common.skc_dport);
printf("TCP connect: %s:%d -> %s:%d\n", $saddr, $sport,
$daddr, $dport);
kprobe:tcp_connect {

$saddr = ntop(2, $sk->__sk_common.skc_rcv_saddr);
$daddr = ntop(2, $sk->__sk_common.skc_daddr);
$sport = (bswap($sk->__sk_common.skc_num));
$dport = (bswap($sk->__sk_common.skc_dport));
printf("TCP connect: %s:%d -> %s:%d\n", $saddr, $sport,

    $daddr, $dport);
↩→

}

since line 13 contradicts line 15 in fig. 7, and line 12 contradicts line 16, the symbolic verification engine identifies the program as invalid.

KEN's feedback loops perform another iteration of synthesis, adding error messages indicating the failed assert statements to the prompt. This time, the Synthesis Engine creates the synthesized program in fig. 8, with sport and dport variables correctly assigned in host byte order. The Comprehension Engine identifies the same assume and assert statements as were identified in fig. 7. On this iteration, the new candidate program is passed to the symbolic verifier, the verifier determines that the candidate eBPF program is correct. Furthermore, the eBPF verifier confirms that the candidate contains no security issues, so the developer can safely extend their kernel with the new program.

System
A
FP
FN
ChatGPT-4
30%
2.5%
67.5%
KEN
80%
2.5%
17.5%

## 5 Evaluation We Implemented A Prototype Of Ken And Used It To Answer The Following Research Questions:

- *RQ1* How effective is KEN at synthesizing eBPF programs for representative eBPF prompts?
- *RQ2* How does each aspect of KEN's design contribute
to the system's accuracy?
- *RQ3* What are the performance, privacy, and cost tradeoffs from using different LLM implementations for KEN?

KEN employs ChatGPT4 as its LLM unless otherwise specified. Additionally, unless otherwise specified, we train the system using KernelCompDataset and the set of prompteBPF program pairs from eBPFNLDataset that were scrapped from the popular web blog [24] and test the system using the set of prompt-eBPF program pairs from eBPFNLDataset that we created anew. We create a baseline that synthesizes eBPF programs using a single prompting of ChatGPT-4 and verifies the output eBPF program by using the built-in eBPF verifier.

Since each prompt can be correctly implemented in multiple ways, we manually inspect KEN's synthesized eBPF program for each prompt to determine if the output correctly implements the prompt. We calculate the Accuracy (A)
of KEN for each experiment, which is the fraction of prompts for which KEN synthesized a correct eBPF program.

To understand the consequence of KEN's incorrect outputs, we split the prompts for which KEN fails to correctly synthesize an eBPF program into two categories: False Negative (FNs), which are the percentage of prompts for which KEN fails to synthesize a verified eBPF program, and False Positives (FPs), which are the percentage of prompts for which KEN synthesizes a verified eBPF program that does not correctly implement the prompt. Conceptually, FPs represent a safety violation since a developer using KEN may extend their kernel incorrectly when KEN produces a false positive. In contrast, FNs represent a liveness violation since a developer is effectively unable to use KEN for such prompts.

5.1
RQ1: KEN Effectiveness For each prompt in the eBPFNLDataset testing set, fig. 9 shows a bar depicting the percentage of time that KEN and the ChatGPT-4 baseline are accurate, produce a false positive, and produce false negative across 10 iterations of the prompt.

Table 1 shows the average number of prompts on which each system is accurate, has a false positive, and produces a false negative for each trial. On average, KEN achieves an accuracy of 80%, which is a factor of 2.67 better than the ChatGPT-4 accuracy of 30%. Moreover, KEN achieves the accuracy improvement without increasing the False Positive rate—both systems achieve an FP rate of only 2.5%.

Inspecting the results for each individual test case, we observe that KEN generates a correct program more often than the baseline in 37 of the 40 test cases. In 11 of 40 test cases, KEN improves the accuracy rate by more than a factor of 9 (i.e., the accuracy rate improves from at most 10% in the baseline to at least 90% in KEN). In addition, KEN improves on the false positive rate in 6 of the 9 test cases in which either system observes a false positive.

## 5.2 Rq2: The Effectiveness Of Ken'S Design Decisions We First Evaluate The Impact Of Each Of Ken'S High-Level Design Decisions, Then Describe An Experiment Showing The Benefit Of Ken'S Comprehension And Symbolic Execution

System
A
FP
FN
ChatGPT-4
30%
2.5%
67.5%
ChatGPT-4+Feedback
60%
7.5%
32.5%
ChatGPT-4+Feedback+Symbex
77.5%
5%
17.5%
KEN
80%
2.5%
17.5%

engines, and finally describe the impact of synthesizing eBPF programs to use bpftrace instead of libbpf.

5.2.1
Effectiveness of KEN's High-Level Design Decisions. Table table 3 shows how each high-level design decision impacts KEN's effectiveness. Each row in the table represents a different configuration. We start from the ChatGPT-4 baseline and apply KEN's design features in the the order of largest impact on accuracy. Namely, we first include KEN's model-guided feedback (feedback), then KEN's comprehension and symbolic execution components (symbex), and finally add training using the blog-gathered portion of the eBPFNLDataset dataset. We note that it is not meaningful to separate KEN's comprehension engine from its symbolic execution components.

The results indicate that model-guided feedback plays a large role in improving the accuracy of KEN, as it improves the accuracy by a factor of 2 (from 30%to 60%). However, this increase in accuracy comes with a factor of 3 increase in false positive rate (from 2.5% to 7.5%). Including the comprehension engine and symbolic execution component also improves KEN's effectiveness substantially—accuracy improves to 77.5%, while the false positive rate moves to 5%. Including the eBPFNLDataset dataset in training comes with a relatively small impact on KEN's accuracy—it only improves by 2.5%. However, training using the eBPFNLDataset dataset does bring KEN's false positive rate back down to the baseline of 2.5%
5.2.2
Effectiveness of KEN's Comprehension and Symbolic Execution Engine. We create a baseline that replaces KEN's automated reasoning components (i.e., the comprehension and symbolic execution engines) with developer expertise to identify the power of KEN's automated reasoning. In particular, we augment the eBPFNLDataset testset by adding the correct kprobe and kretprobe locations for each of the prompts in the eBPFNLDataset testset. Then, we produce a *human expertise* baseline by using the augmented dataset as input to the ChatGPT-4 + feedback + dataset baseline.

table 4 shows the effectiveness of the human expertise baseline compared to KEN. We find that KEN has higher accuracy, without adding additional false positives, compared

System
A
FP
FN
Human Expertise
72.5%
2.5%
25%
KEN
80%
2.5%
17.5%

to the human expertise baseline. KEN's superiority is particularly surprising since KEN does not directly pass the output of the comprehension and symbolic execution engines into its synthesis engine. Our hypothesis is that KEN's feedback loop, initiated on each symbolic execution failure, provides the synthesis engine with sufficient knowledge to replace the human expertise from the baseline. Thus, we find a powerful synergy between KEN's feedback feature and its automated reasoning features.

5.2.3
Effectiveness of using bpftrace instead of libbpf.

We also evaluate the impact of synthesizing programs that use bpftrace compared to synthesizing programs using libbpf. Conventional wisdom is that libbpf implementations are more flexible than bpftrace implementations (i.e., a developer can implement more tasks), but also have more programming complexity [26]. We evaluate KEN's ability to synthesize eBPF programs that use bpftrace and libbpf. However, we find that KEN's symbolic execution engine rarely terminates on libbpf programs because of state explosion due to the frequently use of helper function in libbpf programs. Nonetheless, we calculate the accuracy of KEN when we do not use KEN's comprehension and symbolic execution engines and determine that the accuracy of libbpf programs is 37.5%, whereas the accuracy of bpftrace programs is 60%. Additionally, we calculate the latency of each KEN prompt and find that libbpf programs take an average of 2.16 seconds to synthesize, whereas KEN can synthesize bpftrace programs in an average of 1 second. We conclude that bpftrace is a better synthesis target for our eBPF use cases.

5.3
RQ3: The Performance-Cost-Privacy tradeoffs of alternative LLM models In this section, the performance of KEN is assessed across several recent Large Language Models (LLMs), each presenting distinct potentials for privacy leakage and execution time cost tradeoffs since we expect running locally won't hurt the experience and lower the accuracy that much. We aim to deconstruct both CPU and GPU time to determine the extent of time savings achieved by offloading to remote, given that the CPU time is predominantly consumed by Z3 and the GPU time is primarily allocated for inference. The system is executed on a commercially available Intel 12900K with 96GB DRAM installed and Nvidia Geforce 4090 with 24GB
VRAM. We are utilizing the Python profiling tools SCALENE
[6] for getting the Max VRAM occupation and CPU GPU
time for different models, CodeLLama[50], WizardLM[40]
with 7B and 13B parameter size in Fig. 5.

| Type          | TP %       |
|---------------|------------|
| Inference     |            |
| time          |            |
| Max           |            |
| VRAM(GB)      |            |
| CodeLLama-7B  |            |
| 12.5%         | 3m22.971s  |
| CodeLLama-13B |            |
| 15%           | 5m55.860s  |
| WizardLM-7B   |            |
| 5%            | 10m3.396s  |
| WizardLM-13B  |            |
| 12.5%         | 46m37.193s |

Since the Z3 CPU time is interleaved within other thread waiting times in the Python profiler, we estimate the time function-wise by running the overall Z3 function calling time and Inference function time for one query. We found that Z3 running time corresponds to the assume and sassert number and takes less than 10s for most of the queries. While the 13B model can be accommodated within the 4090 VRAM, the 7B model proves to be more practical owing to its superior inference speed. The 4090 is deployed with fp8 inference quantization using transformers pipeline as a high-level helper. For CodeLLama, we use model "TheBloke/CodeLlama- Instruct-GPTQ"; for WizardLM, we use "WizardLM/WizardCoder- Python-V1.0". We observed that when WizardLM models are deployed locally, VRAM is almost completely utilized. The transformer pipeline alternates between memory and VRAM to accommodate the model size for inference. We notice a performance gain of 1.2× TP in CodeLLama but at the cost of
1.5× more time, and in WizardLM, a gain of 2.5× TP occurs but with a 4.6× increase in time cost. The suboptimal performance observed with fewer parameters is due to the model easily losing context and generating incorrectly formatted text. Compared with CodeLLama-34B's 42.5%, which is 3x-6x of the locally deployed ones, we think offloading LLM to the remote servers is a better solution.

6
Related Work KEN builds on related work in synthesis, verification, and large language models. This section focuses its discussion on related work that has not been discussed elsewhere in the paper; section 2 provides more context for the individual techniques that KEN employs.

KEN builds on decades of work into program synthesis [2, 28, 33, 52, 58], using large language models as advocated by many recent works [3, 10, 21, 38]. KEN's key differences from this prior work is its novel use of a program comprehension and symbolic execution to add assurance that synthesized programs are semantically correct. One key reason for this differences is that KEN targets kernel extension, in which an incorrectly synthesized program can have extremely bad consequences. One additional difference between our work and these prior works is that eBPF is significantly less popular compared to the languages tested by existing work (e.g., python), so our work necessitated developing new datasets.

Recently, Self-Debugging integrated Large Language Models with feedback loops to synthesize programs [12].

The system has a synthesis and feedback structure to KEN.

However, the system uses unit tests and code explanation modules to validate synthesized programs instead of KEN's symbolic execution. Additionally, Self-Debugging targets python and SQL synthesis instead of KEN's eBPF target.

Automated program comprehension determines properties of a program's execution without requiring developer effort. Early work [44] uses a counter-example driven approach, which observe a program under test and derive invariants that hold over all executions. Such systems require a large corpus of test to ensure coverage of the invariants in the program; KEN's approach instead learns less accurate invariants from the original source code. Recent works shows that LLMs are effective at program comprehension tasks [1, 20, 21, 45, 63, 67]. However, the output of existing LLM-based tools is typically an English description of the program which cannot be passed to program verification tools such as symbolic execution.

Like KEN, many systems have embraced machine learning and large language models to enhance developer tools. For example, Neural Fuzzing [53] uses a neural network trained to identify bugs in operating systems more effectively and improves runtime coverage compared to traditional coverageguided fuzzing tools. As another example, Scalene [6] recently began producing LLM-synthesized patches for performance bugs that are found by the profiler.

Many prior works have identified and tried to address verification issues in eBPF. Jia et al. identify challenges that arise in existing eBPF verification due to the large use of helper functions in modern systems [36]. The authors advocate for the use of safe languages (e.g., Rust) to build future kernel extensions. KEN takes an alternative approach to improve on safety by using symbolic execution and Hoare-logic contracts. K2 [64] uses synthesis techniques to optimize the performance of eBPF programs that are passed to the system while ensuring that the optimized programs still pass eBPF's verifier. Thus, whereas KEN's semantic verification provides additional assurances over the eBPF verifier, K2 provides the same safety assurances as the eBPF verifier.

## 7 Conclusion

In conclusion, we presented KEN, a system that helps developers extend their kernels using eBPF by allowing Kernel Extensions written in Natural language. KEN uses recent advances in large language models (LLMs) (e.g., OpenAI's InstructGPT[43], *HumanEval*[11], and *ChatGPT*[55]) to synthesis an eBPF program given a user's English language prompt. A user can then extend their kernel by injecting