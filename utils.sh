assemble() {
    asm=$1
    filename=$2
    echo ".intel_syntax noprefix" > asm-tmp.s
    echo "$asm" >> asm-tmp.s
    sed -i "
        s/|15/.byte 0x66,0x66,0x66,0x66,0x66,0x66,0x2e,0x0f,0x1f,0x84,0x00,0x00,0x00,0x00,0x00;/g
        s/|14/.byte 0x66,0x66,0x66,0x66,0x66,0x2e,0x0f,0x1f,0x84,0x00,0x00,0x00,0x00,0x00;/g
        s/|13/.byte 0x66,0x66,0x66,0x66,0x2e,0x0f,0x1f,0x84,0x00,0x00,0x00,0x00,0x00;/g
        s/|12/.byte 0x66,0x66,0x66,0x2e,0x0f,0x1f,0x84,0x00,0x00,0x00,0x00,0x00;/g
        s/|11/.byte 0x66,0x66,0x2e,0x0f,0x1f,0x84,0x00,0x00,0x00,0x00,0x00;/g
        s/|10/.byte 0x66,0x2e,0x0f,0x1f,0x84,0x00,0x00,0x00,0x00,0x00;/g
        s/|9/.byte 0x66,0x0f,0x1f,0x84,0x00,0x00,0x00,0x00,0x00;/g
        s/|8/.byte 0x0f,0x1f,0x84,0x00,0x00,0x00,0x00,0x00;/g
        s/|7/.byte 0x0f,0x1f,0x80,0x00,0x00,0x00,0x00;/g
        s/|6/.byte 0x66,0x0f,0x1f,0x44,0x00,0x00;/g
        s/|5/.byte 0x0f,0x1f,0x44,0x00,0x00;/g
        s/|4/.byte 0x0f,0x1f,0x40,0x00;/g
        s/|3/.byte 0x0f,0x1f,0x00;/g
        s/|2/.byte 0x66,0x90;/g
        s/|1/nop;/g
        s/|//g
    " asm-tmp.s
    as asm-tmp.s -o asm-tmp.o || exit
    objcopy asm-tmp.o -O binary "$filename"
    rm asm-tmp.*
}
