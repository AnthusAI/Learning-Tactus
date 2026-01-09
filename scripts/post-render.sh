#!/usr/bin/env bash
set -euo pipefail

project_dir="${QUARTO_PROJECT_DIR:-$(pwd)}"
output_dir="${QUARTO_PROJECT_OUTPUT_DIR:-_output}"

cover_src="${project_dir}/cover.html"
index_dst="${output_dir}/index.html"
animal_dst_dir="${output_dir}/images"

if [[ ! -f "${cover_src}" ]]; then
  echo "post-render: missing cover source: ${cover_src}" >&2
  exit 1
fi

if [[ ! -d "${output_dir}" ]]; then
  echo "post-render: output dir not found: ${output_dir} (skipping)" >&2
  exit 0
fi

if [[ ! -f "${index_dst}" ]]; then
  # Non-HTML renders may not produce an index.html.
  exit 0
fi

cp "${cover_src}" "${index_dst}"

animal_src=""
if [[ -f "${project_dir}/images/cover-animal.png" ]]; then
  animal_src="${project_dir}/images/cover-animal.png"
elif [[ -f "${project_dir}/cover-animal.png" ]]; then
  animal_src="${project_dir}/cover-animal.png"
fi

if [[ -n "${animal_src}" ]]; then
  mkdir -p "${animal_dst_dir}"
  cp "${animal_src}" "${animal_dst_dir}/cover-animal.png"
fi
