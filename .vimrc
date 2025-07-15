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
nnoremap <leader>e :Lexplore<CR>

" Install and use Oxocarbon colorscheme via vim-plug
call plug#begin('~/.vim/plugged')
Plug 'nyoom-engineering/oxocarbon.nvim'
call plug#end()

colorscheme oxocarbon

set clipboard=unnamedplus
