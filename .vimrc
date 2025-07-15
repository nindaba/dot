" Enable relative line numbers
set relativenumber
set number

" Use two spaces for tabs
set tabstop=2
set shiftwidth=2
set expandtab

" Set leader key to space
let mapleader=" "

" Map <leader>e to toggle the built-in netrw file tree
nnoremap <leader>e :Explore<CR>

" Install and use Oxocarbon colorscheme via vim-plug
" call plug#begin('~/.vim/plugged')
" Plug 'nyoom-engineering/oxocarbon.nvim'
" call plug#end()
source https://www.vim.org/scripts/download_script.php?src_id=14080 " Carbon theme

colorscheme oxocarbon

set clipboard=unnamedplus

" Change cursor shape based on mode
let &t_SI = "\e[6 q"   " Insert mode: steady vertical bar
let &t_EI = "\e[2 q"   " Normal mode: steady block
