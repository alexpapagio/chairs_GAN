# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Generate lerp videos using pretrained network pickle."""

import copy
import os
import re
from typing import List, Optional, Tuple, Union

import click
import dnnlib
import imageio
import numpy as np
import scipy.interpolate
import torch
from tqdm import tqdm

import legacy

# ----------------------------------------------------------------------------


def layout_grid(
    img, grid_w=None, grid_h=1, float_to_uint8=True, chw_to_hwc=True, to_numpy=True
):
    batch_size, channels, img_h, img_w = img.shape
    if grid_w is None:
        grid_w = batch_size // grid_h
    assert batch_size == grid_w * grid_h
    if float_to_uint8:
        img = (img * 127.5 + 128).clamp(0, 255).to(torch.uint8)
    img = img.reshape(grid_h, grid_w, channels, img_h, img_w)
    img = img.permute(2, 0, 3, 1, 4)
    img = img.reshape(channels, grid_h * img_h, grid_w * img_w)
    if chw_to_hwc:
        img = img.permute(1, 2, 0)
    if to_numpy:
        img = img.cpu().numpy()
    return img


# ----------------------------------------------------------------------------


def gen_interpolate_of_pair(G, w_a_npz, w_b_npz, w_frames, device):

    # gen_video would start by initialising the seeds, but we don't want that, we want
    # to use our provided w vectors
    #
    # Load w vectors
    # which are the latent vectors for the images we want to interpolate between
    # output of projected_w.unsqueeze(0).cpu().numpy()
    # stored in a single key dict, where "w" points to the vector
    w_a = np.load(w_a_npz)["w"]
    w_b = np.load(w_b_npz)["w"]
    print("w_a.shape, w_b.shape", w_a.shape, w_b.shape)

    # save images
    w_a_tensor = torch.from_numpy(w_a).to(device)
    w_b_tensor = torch.from_numpy(w_b).to(device)

    # turn images into size-1 batches
    batch_a = w_a_tensor.unsqueeze(0)
    batch_b = w_b_tensor.unsqueeze(0)
    img_a = G.synthesis(ws=batch_a, noise_mode="const")[0]
    img_b = G.synthesis(ws=batch_b, noise_mode="const")[0]

    # ws = torch.stack([w_a_tensor, w_b_tensor])

    # Interpolation.
    grid = []
    for yi in [0]:
        row = []
        for xi in [0]:
            x = [-1, 0]
            y = np.tile(ws[0][0].cpu().numpy(), [2 + 1, 1, 1])
            interp = scipy.interpolate.interp1d(x, y, kind="cubic", axis=0)
            row.append(interp)
        grid.append(row)


#     # Render video.
#     video_out = imageio.get_writer(
#         mp4, mode="I", fps=60, codec="libx264", **video_kwargs
#     )
#     for frame_idx in tqdm(range(num_keyframes * w_frames)):
#         imgs = []
#         for yi in range(grid_h):
#             for xi in range(grid_w):
#                 interp = grid[yi][xi]
#                 w = torch.from_numpy(interp(frame_idx / w_frames)).to(device)
#                 img = G.synthesis(ws=w.unsqueeze(0), noise_mode="const")[0]
#                 imgs.append(img)
#         video_out.append_data(
#             layout_grid(torch.stack(imgs), grid_w=grid_w, grid_h=grid_h)
#         )
#     video_out.close()


# ----------------------------------------------------------------------------


@click.command()
@click.option("--network", "network_pkl", help="Network pickle filename", required=True)
@click.option(
    "--w_a_npz",
    "w_a_npz",
    help="Image A w vector approximation's NPZ filepath",
    required=True,
)
@click.option(
    "--w_b_npz",
    "w_b_npz",
    help="Image B w vector approximation's NPZ filepath",
    required=True,
)
@click.option(
    "--w-frames",
    type=int,
    help="Number of frames to interpolate between latents",
    default=10,
)
def generate_images(network_pkl: str, w_a_npz: str, w_b_npz: str, w_frames: int):
    """Render a latent vector walk between image points A and B."""

    print(f'Loading networks from "{network_pkl}"...')
    device = torch.device("cuda")
    with dnnlib.util.open_url(network_pkl) as f:
        G = legacy.load_network_pkl(f)["G_ema"].to(device)  # type: ignore

    gen_interpolate_of_pair(
        G=G,
        w_a_npz=w_a_npz,
        w_b_npz=w_b_npz,
        w_frames=w_frames,
        device=device,
    )


# ----------------------------------------------------------------------------

if __name__ == "__main__":
    generate_images()  # pylint: disable=no-value-for-parameter

# ----------------------------------------------------------------------------
