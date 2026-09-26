"""Controlled demonstration of multimodal state reconstruction.

This is an engineering experiment, not biological evidence.
"""
import numpy as np

from ceh.multimodal import concatenate_modalities, modality_agreement

def main() -> None:
    molecular = np.array([0.8, 0.2, 0.4])
    imaging = np.array([0.7, 0.3, 0.5])
    state = concatenate_modalities(molecular, imaging)
    agreement = modality_agreement(molecular, imaging)

    print("combined_state_dimension:", state.size)
    print("cross_modal_agreement:", round(agreement, 4))

if __name__ == "__main__":
    main()
