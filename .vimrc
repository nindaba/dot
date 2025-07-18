" Enable relative line numbers
set relativenumber
set number

" Use two spaces for tabs
set tabstop=2
set shiftwidth=2
set expandtab

" Remove the spliting lines
set fillchars=vert:\ ,horiz:\ ,fold:\ ,eob:\ 

" Set leader key to space
let mapleader=" "

" Map <leader>e to toggle the built-in netrw file tree
nnoremap <leader>e :Explore<CR>
nnoremap <Leader>+ :resize +5<CR>
nnoremap <Leader>- :resize -5<CR>
nnoremap <Leader>> :vertical resize +5<CR>
nnoremap <Leader>< :vertical resize -5<CR>
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l


" Install and use Oxocarbon colorscheme via vim-plug
" call plug#begin('~/.vim/plugged')
" Plug 'nyoom-engineering/oxocarbon.nvim'
" call plug#end()
"Exception source https://www.vim.org/scripts/download_script.php?src_id=14080 " Carbon theme

" colorscheme oxocarbon

set clipboard=unnamedplus

" Change cursor shape based on mode
let &t_SI = "\e[6 q"   " Insert mode: steady vertical bar
let &t_EI = "\e[2 q"   " Normal mode: steady block

" Highlight yanked text for 200ms
augroup YankHighlight
  autocmd!
  autocmd TextYankPost * silent! lua vim.highlight.on_yank {timeout = 200}
augroup END

let g:netrw_liststyle = 3
