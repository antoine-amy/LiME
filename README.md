# Muon Decay Experiment Analysis

This analysis focuses on extracting the decay constant (tau) and understanding the associated errors.

## Error Measurement on Tau

### Error Bars on the Fit
- **In Time (x-axis)**: Errors include a systematic error of ±0.078mV (to be converted into time), accounting for the calibration of the Time-to-Amplitude Converter (TAC).
- **In Count (y-axis)**: Purely statistical errors, calculated using the standard deviation (sigma). The chi-square (\(\chi^2\)) of the fit should also be considered to assess the fit's quality.

## Digital Conversion Limit Explanation

A digital conversion limit of 0.078mV is noted, stemming from a 256-level quantization over a ±10V range. This quantization introduces noise in the 0-0.078mV range. To ensure signal integrity, a conservative lower threshold of 0.100mV is set, making the first bin effectively represent signals in the 0.100-0.156mV range. A 50% error margin is applied to the 0.156mV value to account for these considerations.

## Background Noise and Coincidental Events

To account for background noise and coincidental events, the mean (and standard deviation) is calculated from a time point where muon decay becomes improbable (e.g., past 100 microseconds) to the end of the measurement period. This background is subtracted from the exponential decay bins, with adjustments made for bin width. The error in this background mean, added to the initial error, accounts for variability in background noise levels.

## Handling of the First Bin

The first bin is not removed, but significant errors in both x (time) and y (count) are acknowledged:
- **Error in x**: Includes TAC calibration (±0.1ns), TAC precision (±5%), and digitization precision (±0.078mV).
- **Error in y**: Calculated with a 5-sigma criterion and includes the subtraction of background noise.

## Error in the Fit

The uncertainty in the fit parameters is derived from the covariance matrix obtained during the curve fitting process. This matrix provides a quantitative measure of the parameter estimates' reliability, crucial for understanding the fit's precision and the decay constant's accuracy.

## Conclusion

This analysis method provides a framework for accurately determining the decay constant of muons from experimental data, with a comprehensive approach to error estimation and background noise treatment. By addressing both statistical and systematic errors, the methodology ensures a robust understanding of the muon decay process and the experimental data's inherent uncertainties.
