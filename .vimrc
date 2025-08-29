" Set folds
set foldmethod=syntax
set foldlevel=99

" Set directory for swap files
set directory^=~/dev/vswp//

" Set base path
set path+=**/*
" Enable relative line numbers
set relativenumber
set number

" Use two spaces for tabs
set tabstop=2
set shiftwidth=2
set expandtab

" Remove the spliting lines
set fillchars=vert:\ 
highlight VertSplit cterm=NONE

" Search Highlight
set hlsearch
highlight Search ctermfg=white
" Set leader key to space
let mapleader=" "

" Map <leader>e to toggle the built-in netrw file tree
nnoremap <leader>e :w<CR>:e .<CR>
nnoremap <Leader>+ :resize +15<CR>
nnoremap <Leader>- :resize -15<CR>
nnoremap <Leader>> :vertical resize +15<CR>
nnoremap <Leader>< :vertical resize -15<CR>
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l
nnoremap tt :wa \| terminal<CR>
nnoremap S :wa<CR>
nnoremap <leader>noh :noh<CR>
nnoremap cc :ccl<CR>
nnoremap ck :cp<CR>
nnoremap cj :cn<CR>

"nnoremap kj <Esc>
"nnoremap jk <Esc>

" Install and use Oxocarbon colorscheme via vim-plug
" call plug#begin('~/.vim/plugged')
" Plug 'nyoom-engineering/oxocarbon.nvim'
" call plug#end()
"Exception source https://www.vim.org/scripts/download_script.php?src_id=14080 " Carbon theme

" colorscheme oxocarbon

" Completion settings
set complete=.,w,b,u,t,i
set completeopt=menu,menuone,noselect,noinsert,preview

" Key mappings for navigating the popup menu
inoremap <expr> <C-j> pumvisible() ? "\<C-n>" : "\<C-j>"
inoremap <expr> <C-k> pumvisible() ? "\<C-p>" : "\<C-k>"
inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<CR>"

set updatetime=250
autocmd CursorHoldI * if col('.') > 2 && !pumvisible() | call feedkeys("\<C-n>", 'n') | endif

" Change cursor shape based on mode
let &t_SI = "\e[6 q"   " Insert mode: steady vertical bar
let &t_EI = "\e[2 q"   " Normal mode: steady block

" Highlight yanked text for 200ms
augroup YankHighlight
  autocmd!
  autocmd TextYankPost * silent! lua vim.highlight.on_yank {timeout = 200}
augroup END

let g:netrw_liststyle = 3


" Warnings 
set noerrorbells
set novisualbell


" Find in files using grep
command! -nargs=1 Find call s:GrepToQuickfix(<f-args>)
nnoremap <Leader>f :Find<Space>

function! s:GrepToQuickfix(term)
  let l:cmd = 'grep -rn "' . a:term . '" . > /tmp/vim_grep_results.txt'
  call system(l:cmd)
  cgetfile /tmp/vim_grep_results.txt
  copen
endfunction


" Navigation

" Enable search highlighting and incremental search
set hlsearch
set incsearch
set ignorecase
set smartcase
set number

" Clear search highlight with double <Esc>
nnoremap <Esc><Esc> :nohlsearch<CR>

" Use 's' to start a word search (case-insensitive)
nnoremap <leader>s /<C-r>=input("Search word: ")<CR><CR>

" Optional: Highlight matches manually with <Leader>h
function! HighlightMatches()
  let @/ = input("Highlight word: ")
  set hlsearch
endfunction
nnoremap <Leader>h :call HighlightMatches()<CR>


" Find files by name using 'find' and show results in quickfix
command! -nargs=1 FindFile call s:FindFilesByName(<f-args>)
nnoremap <Leader>f :FindFile<Space>

function! s:FindFilesByName(term)
  " Use find to locate files with the term in their name (case-insensitive)
  
  
  let l:cmd = 'find . -type f -iname "*' . a:term . '*" | sed "s/$/:1: /" > /tmp/vim_find_results.txt'
  
  call system(l:cmd)

  " Load results into quickfix list
  cgetfile /tmp/vim_find_results.txt
  copen
endfunction




