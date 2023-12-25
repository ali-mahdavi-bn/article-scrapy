# Noise Spectrum Estimation With Improved Minimum Controlled Recursive Averaging Based On Speech Enhancement Residue

Dalei Wu, Wei-Ping Zhu and M.N.S. Swamy Department of Electrical and Computer Engineering, Concordia University
1455 Maisonneuve Blvd. West, Montreal, QC, H3G 1M8, Canada Email: {daleiwu, weiping, swamy}@ece.concordia.ca

  Abstract— The conventional soft-decision based noise estima-
tion algorithms normally assume that noise exists, only when
speech is absent. Consequently, the estimated noise spectra are
not updated in the segments of speech presence, but only in
those of speech absence. This assumption often results in several
problems such as delay and bias of noise spectrum estimates. In
this paper, we propose a solution by using speech enhancement
residue (SER) to compensate the estimation bias in the presence
of speech. The proposed method can be naturally combined with
the improved minimum controlled averaging (IMCRA) method to
consistently update noise spectra. The experimental results show
that the SER-based IMCRA can reduce the relative segmental
estimation errors for various types of noise at different SNR
levels, especially for car internal noise.

## I. Introduction

Noise spectrum estimation techniques are widely used in a wide range of speech processing applications, e.g., speech enhancement, speech recognition [4], [2] and speaker recognition [8], [9]. Generally speaking, they can be classified into two groups: hard techniques and soft techniques. The hard techniques estimate noise spectra using only the noise segments of a noisy speech signal, which are often identified by a method of voice activity detection (VAD). The soft noise estimation techniques estimate noise spectra by using uncertainty or probability which considers possible contributions from both speech and noise segments of the noisy signal. Hence, the soft methods are normally more accurate than the hard techniques.

Three main methods for the soft noise estimation techniques are worth noting: minimum statistics (MS) [6], minimum controlled recursive averaging (MCRA) [2] and improved minimum contorlled recursive averaging (IMCRA) [3]. In the MS method, Martin et al. firstly proposed to search a given window of frames for the minimal value of the smoothed power spectra of a noisy signal, and then the minimum power spectrum is multiplied by a factor to give an estimate of the noise spectrum. In [2], [3], Cohen et al. proposed MCRA and its improved version, IMCAR, to improve the MS by employing a two-stage search strategy that makes use of the estimated speech presence probability.

However, these methods normally assume that noise exists, only when speech is absent. In other words, these noise estimators are only updated for the segments of noise presence, but not for those of speech presence. This assumption often results in several problems such as:(1) noise spectrum estimates have certain delays and the delays become larger for time variant noise. (2) nonstaionary noise cannot be successfully estimated, especially when the noise changes in a fast speed. (3) The estimators are often biased and therefore not very accurate.

In this paper, we propose several modifications to fix the problems aforementioned in IMCRA. First, we modify the mechanism of the time variant recursive averaging of IMCRA to utilize both noise and speech segments. Second, SER is proposed to serve as an approximation to true noise and used in the recursive averaging procedure to update noise spectra in the case of speech presence. The derived method is referred to as SER-based IMCRA.

The proposed method has been evaluated for a variety of types of noise and input SNR levels. The experimental results have showed the proposed modifications are able to improve the performance of IMCRA considerably.

## Ii. Overview Of Improved Minimum Controlled Recursive Averaging

IMCRA is a time-varying averaging procedure to recursively update noise spectra. In estimation, it considers the uncertainty or probability of a frame being recognized as noise. The probability is estimated by using a two-stage minimum controlled searching module.

More specifically, the goal of the IMCRA is to estimate the noise spectra

$$\bar{\lambda}_{d}(k,\ell), \tag{1}$$
for the kth frequency bin and the ℓth frame, where d denotes the noise in a given signal.

## A. Time-Varying Recursive Averaging

The recursive averaging procedure is to estimate λd(*k, ℓ* +
1), based on two hypotheses H0 and H1, which represent the noise and speech, respectively, for the current ℓth frame.

For hypothesis H0 (noise), the averaging formula is a linear combination of the noise estimation at the ℓ-th frame and an update according to the squared power spectra of the current ℓth frame.:

$$H_{0}(k,\ell):\bar{\lambda}_{d}(k,\ell+1)=\alpha_{d}\bar{\lambda}_{d}(k,\ell)+(1 -\alpha_{d})|Y(k,\ell)|^{2}, \tag{2}$$ where $Y(k,\ell)$ is the spectrum of the noisy signal for the $k$th frequency bin and the $\ell$th frame.

For hypothesis $H_{1}$ (speech), the averaging has no update, i.e.,

$$H_{1}(k,\ell):\bar{\lambda}_{d}(k,\ell+1)=\bar{\lambda}_{d}(k,\ell). \tag{3}$$
By introducing the priori speech absence (noise) probability
(SAP) q(*k, ℓ*) = P(H0(*k, ℓ*)) and speech presence (speech)
probability (SPP) p(*k, ℓ*) = P(H1(*k, ℓ*)), and merging these two hypotheses, we then have the merged averaging equation as follows:

$$\tilde{\lambda}_{d}(k,\ell+1)=\tilde{\alpha}_{d}(k,\ell)\tilde{\lambda}_{d}(k, \ell)+[1-\tilde{\alpha}_{d}(k,\ell)]|Y(k,\ell)|^{2}, \tag{4}$$

where

$$\tilde{\alpha}_{d}(k,\ell)=\alpha_{d}+(1-\alpha_{d})p(k,\ell). \tag{5}$$
and αd is a smoothing parameter.

## B. Minimum Controlled Estimation

The SAP q(*k, ℓ*) and SPP p(*k, ℓ*) are estimated at the second step, which is referred to as minimum controlled estimation (MCE). MCE is a two-stage searching procedure.

At the first stage, a coarse decision is made to identify the speech and noise segments in the noisy speech signal. This process consists of four steps: (1) noisy spectra are smoothed in frequency and time domain to obtain S(*k, ℓ*). (2) Searching for the minimum Smin(*k, ℓ*) of the smoothed noisy power spectra in a given size of a window. (3) Defining γmin(*k, ℓ*)
(posterior SNR) and ζ(*k, ℓ*) (smoothed prior SNR) as

$$\gamma_{min}\left(K,\ell\right)\stackrel{{\Delta}}{{=}}\frac{|Y(k, \ell)|^{2}}{B_{min}S_{min}(k,\ell)} \tag{6}$$

$$\zeta(k,\ell)\stackrel{{\Delta}}{{=}}\frac{S(k,\ell)}{B_{min}S_{ min}(k,\ell)} \tag{7}$$
where Bmin is a bias of the noise estimate, which is set to
1.66. (4) Decision is made according to the criterion

$$I(k,\ell)=\left\{\begin{array}{ll}1,&\mbox{if }\gamma_{min}(k,\ell)<\gamma_{0}\\ &\mbox{and }\zeta(k,\ell)<\zeta_{0},\\ 0,&otherwise,\end{array}\right. \tag{8}$$

where $\gamma_{0}=4.6$ and $\zeta_{0}=1.67$.

The second stage is fine searching, which only uses the noise parts identified by the first pass searching. At this stage, the SAP and SPP are calculated with similar operations: (1) noisy spectra $\tilde{S}(k,\ell)$ are only smoothed in time domain (not in frequency domain). (2) searching for the minimum of the smoothed noisy spectra $\tilde{S}_{min}(k,\ell)$. (3) similarly, defining $\tilde{\gamma}_{min}(k,\ell)$ (posterior SNR) and $\tilde{\zeta}(k,\ell)$ (smoothed prior SNR) as

$$\tilde{\gamma}_{min}(k,\ell)\stackrel{{\triangle}}{{=}}\frac{|Y (k,\ell)|^{2}}{B_{min}\tilde{S}_{min}(k,\ell)} \tag{9}$$

$$\tilde{\zeta}(k,\ell)\stackrel{{\triangle}}{{=}}\frac{S(k,\ell )}{B_{min}\tilde{S}_{min}(k,\ell)}. \tag{10}$$
(4) the SAP is derived by

$$q(k,\ell)=\left\{\begin{array}{ccc}1,&\text{if }\tilde{\gamma}_{min}(k,\ell)<1\\ &\text{and }\tilde{\zeta}(k,\ell)<\zeta_{0},\\ \frac{\gamma_{1}-\tilde{\gamma}_{min}(k,\ell)}{\gamma_{1}-1},&\text{if }1< \tilde{\gamma}_{min}(k,\ell)<\gamma_{1}\\ &\text{and }\tilde{\zeta}(k,\ell)<\zeta_{0},\\ 0,&otherwise,\end{array}\right. \tag{11}$$

where $\gamma_{1}=3$ and $\zeta_{0}=1.67$.

The SPP $p(k,\ell)$ is then obtained according to the equation

$$p(k,\ell)=\left\{1+\frac{q(k,\ell)}{1-q(k,\ell)}(1+\xi(k,\ell))\exp(-v(k,\ell ))\right\}^{-1}, \tag{12}$$

where $v=\gamma\xi/(1+\xi)$, $\gamma$ and $\xi$ are a posteriori and a priori SNR, respectively.

## Iii. Improved Minimum Controlled Recursive Averaging Based On Speech Enhancement Residue

From Section II-A, we can easily see that there is no update for noise spectrum estimation in the case where the speech hypothesis H1 is true, and hence the noise spectra are simply equal to those of the previous frame. This principle is reasonable, only if it is assumed that no noise is contained in the segments, which are identified as *speech*. Though such a situation sometimes appears, mostly other cases occur, where noise and speech coexist. For instance, additive noise is often added to all the segments (voiced and unvoiced) of clean speech to generate noisy speech, but not only to the unvoiced parts. Therefore, the averaging equation for hypothesis H1, e.g., eq. (3), is not very accurate. This phenomenon can be clearly observed in the plot of estimated noise spectra, where the estimated noise spectra for the speech segments are always kept constant, as shown in Fig. 1-(top).

As aforementioned in Section I, this assumption often results in several problems, which are harmful for noise estimation.

## A. Ser-Based Time-Variant Recursive Averaging

One of the solutions to this problem is to design a timevariant recursive averaging mechanism, where noise spectra are updated for both speech and noise segments. In detail, for the noise part (hypothesis H0), we keep the averaging method unchanged, i.e.,

$$H_{0}(k,\ell):\bar{\lambda}_{d}(k,\ell+1)=\alpha_{d}\bar{\lambda}_{d}(k,\ell)+(1- \alpha_{d})|Y(k,\ell)|^{2}. \tag{13}$$

For the speech part (hypothesis $H_{1}$), by introducing a coarse noise spectrum (CNS) $I_{n}(k,\ell)$ for the $k$th frequency bin and the $\ell$th frame, we estimate the $(\ell+1)$th noise spectra by considering the $\ell$th estimate and the contribution of the raw noise spectra $I_{n}(k,\ell)$, i.e.,

$$H_{1}(k,\ell):\bar{\lambda}_{d}(k,\ell+1)=\alpha_{p}\bar{\lambda}_{d}(k,\ell)+ (1-\alpha_{p})|I_{n}(k,\ell)|^{2}, \tag{14}$$

where $\alpha_{p}$ is a smoothing parameter.

Similarly, using SPP $p(k,\ell)$, we can obtain the merged averaging equation as follows:

$$\begin{split}&\bar{\lambda}_{d}(k,\ell+1)=[\alpha_{p}\bar{ \lambda}_{d}(k,\ell)+(1-\alpha_{p})|I_{n}(k,\ell)|^{2}]p(k,\ell)\\ &+[\alpha_{d}\bar{\lambda}_{d}(k,\ell)+(1-\alpha_{d})|Y(k,\ell) |^{2}](1-p(k,\ell)).\end{split} \tag{15}$$
Further, we have

$$\bar{\lambda}_{d}(k,\ell+1)=\tau\bar{\lambda}_{d}(k,\ell)+\phi|I_{n}(k,\ell)|^{2 }+\psi|Y(k,\ell)|^{2}, \tag{16}$$

where

$$\tau =\alpha_{d}+(\alpha_{p}-\alpha_{d})p(k,\ell) \tag{17}$$ $$\phi =(1-\alpha_{p})p(k,\ell)$$ (18) $$\psi =(1-\alpha_{d})(1-p(k,\ell)). \tag{19}$$
From these equations, we can see that: (1) the new averaging scheme is an extension to the old averaging solution. When
αp = 1, the new scheme is reduced to the old averaging solution. (2) as compared to the old solution, the new averaging formula has one extra term related to CNS, i.e., In(*k, ℓ*), which considers the noise component in the "speech" segments of the noisy signal. Based on the observation (2), we can further relax the equation of φ as follows,

$$\dot{\phi}=\left\{\begin{array}{cc}(1-\alpha_{p})p(k,\dot{\epsilon}),&p(k,\dot{ \epsilon})\geq\phi_{0}\\ 0,&p(k,\dot{\epsilon})<\phi_{0},\end{array}\right. \tag{20}$$
where φ0 is a controlled parameter.

Note that the accuracy of CNS seriously affects the performance of the proposed algorithm. We address the issue of how to obtain a proper CNS in the next subsection.

## B. Calculation Of In(*K, ℓ*)

We propose to estimate CNS by using speech enhancement residue (SER). SER is obtained by subtracting the enhanced signal from the original noisy signal, where the enhanced signal is derived using a certain speech enhancement algorithm. For instance, it can be estimated by using the optimally modified log-spectrum amplitude (OMLSA) method [3].

More specifically, let x(ℓ) be the ℓth frame of the original noisy signal, and x∗(ℓ) be the ℓth frame of the clean signal estimated by OMLSA, then In(*k, ℓ*) can be obtained as follows:
I(*k, ℓ*) = {F · [x(ℓ) − x∗(ℓ)]} (k),
(21)
where F is the discrete Fourier transform matrix and k is the frequency bin. The overall structure of the proposed method can be summarized by Fig. 2.

## Iv. Experiments

In this section, we evaluate the performance of the SER-
based method for noise spectrum estimation. As in [3], we choose clean data samples (one sentence of male and one of female) from the TIMIT database [5], downsampled at 8khz. The speech samples are corrupted by various types of noise: stationary white Gaussian noise (S-WGN), nonstationary white Gaussian noise (NS-WGN), car interior noise (CIN) and F16 cockpit noise (FCN). The noises are taken from Noisex92 database [7]. According to [3], [10], a nonstationary WGN is used, which has a constant power spectrum density (PSD) at the first and last one-fifth of the duration of the noise. At the second one-fifth duration, the PSD is linearly increasing to a certain level at a rate of 2*dB/sec*, and again linearly decreasing to the previous level after remaining at the high level for the third one-fifth of the duration.

The noise-corrupted signals have segmental SNRs in the range [−5, 10] dB. The segmental SNR is defined by [3]

SegSNR = 10 k |X(*k, ℓ*)|2 L ℓ∈L log � � � k |D(*k, ℓ*)|2 (22)
where L represents the set of frames that contain speech, L
is the cardinality of L, X(*k, ℓ*) and D(*k, ℓ*) are the spectra at the kth frequency bin and ℓth frame, respectively.

Following [3], we use the criterion of segmental relative estimation errors (SREEs) for experimental evaluation,

SegErr = 1 L � k � ˆλd(k, ℓ) − λd(*k, ℓ*) �2 ℓ=1 L � � k λ2 d(*k, ℓ*) , (23)
where ˆλd(*k, ℓ*) and λd(*k, ℓ*) are the spectra of the estimated and true noise at the kth frequency bin and ℓth frame.

In the experiments, we use a hamming window with the length 256 to preprocess a frame. The frame is shifted by
25% of the window length. The threshold φ0 is set to 0.99
and the smoothing parameter αp is set to 0.998. All the other parameters of IMCRA and OMLSA are kept to the default values, suggested by [2], [3].

## A. Performance For Female Speakers

The SREEs for the female speakers are shown in Fig. 3. In this figure, we can see that the SERRs of SER-IMCRA for the female speakers for all the noise types and levels are lower than those of the conventional IMCRA. The highest reduction
(approximately 10% relative reduction) is observed for the car noise over all the SNR levels. For the nonstationary noise, the improvements are relatively smaller than the other three types of noise.

## B. Performance Of Male Speakers

The SREEs for the male speakers are shown in Fig. 4, from which we can see the SREEs of SER-IMCRA are mostly lower than those of the conventional IMCRA. The highest reduction is similarly achieved for the car noise. This may suggest that this method is particularly powerful to deal with car internal noise.

The effect of the proposed method can be visualized by comparing the top figure (IMCRA) and the bottom figure (SER-IMCRA) of Fig. 1. It clearly demonstrates that the estimated spectra of the SER-IMCRA are much closer to the true noise than the conventional IMCRA, specially in the case of speech presence.

## V. Conclusions

In this paper, we have presented a noise spectrum estimation method for noisy speech signals by using speech enhancement residue. The proposed method modifies the first component of IMCRA with an SER-based time variant recursive averaging to update the estimated noise spectra. Through computer simulations, we have demonstrated that (1) SER contains very useful information for noise spectrum estimation; (2) the modified estimation mechanism is quite effective in estimating noise spectra for various types of noise at different SNR levels, especially in the case of car internal noise.

## References

[1] M.E. Davies, C.J. James, "Source separation using single channel ICA",
Signal Processing, Vol. 87 pp. 1819-1832, 2007.
[2] I. Cohen, "Speech enhancement for nonstationary noise environments",
Signal Process., vol. 81, no. 11, pp. 2403 - 2418, Nov. 2001.
[3] I. Cohen, "Noise Spectrum Estimation in Adverse Environments: Improved Minima Controlled Recursive Averaging", IEEE Trans. Speech Audio Processing, vol. 11, no. 5, pp. 466 - 475, September 2003.
[4] Y. Emphrim and D. Malah, "Speech Enhancement Using a Minimum
Mean-Square Error Short-Time Spectral Amplitude Estimator", IEEE transactions on acoustics, speech and signal processing, Vol. ASSP-32., No. 6, December, 1109 - 1121, 1984.
[5] J. S. Garofolo, "Getting started with the DARPA TIMIT CD-ROM:
An acoustic phonetic continuous speech database", Nat. Inst. Standards
Technol. (NIST), Gaithersburg, MD, prototype as of Dec. 1988.
[6] R. Martin, "Noise power spectral density estimation based on optimal
smoothing and minimum statistics," IEEE Trans. Speech Audio Processing, vol. 9, pp. 504 - 512, July 2001.
[7] A. Varga and H. J. M. Steeneken, "Assessment for automatic speech
recognition: II. NOISEX-92: A database and an experiment to study the effect of additive noise on speech recognition systems", Speech Commun., vol. 12, no. 3, pp. 247-251, 1993.
[8] D. Wu, "α-Gaussian Mixture Model for Speaker Recognition", in: Pattern
Recognition Letters 30 (6), pp. 589-594, 2009.
[9] D. Wu, "Parameter Estimation for α-GMM based on Maximum Likelihood Criterion", in: Neural Computation, vol. 21, no. 6, pp. 1776-1795, 2009.
[10] D. Wu, W.P. Zhu and M.N.S. Swamy, "A compressive sensing method
for noise reduction of speech and audio signals", Proceedings of the MWSCAS, 2011.