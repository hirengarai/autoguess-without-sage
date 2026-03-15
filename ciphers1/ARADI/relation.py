import os

output_dir = os.path.curdir

WORD_BITS = 32
NWORDS = 8
NBITS = NWORDS * WORD_BITS  # 256


def var(round_idx, bit):
    return f"k_{round_idx}_{bit}"


def bit_index(word, bit_in_word):
    return word * WORD_BITS + bit_in_word


def rot_in_word_bitidx(word, bit_in_word, sh):
    # ROL_sh: out[bit] = in[(bit - sh) mod 32]
    return bit_index(word, (bit_in_word - sh) % WORD_BITS)


def perm_words(round_i):
    # From ARADI spec (period 2):
    # P0 = (12)(56)  => swap 1<->2 and 5<->6
    # P1 = (14)(36)  => swap 1<->4 and 3<->6
    if (round_i % 2) == 0:
        return [0, 2, 1, 3, 4, 6, 5, 7]
    return [0, 4, 2, 6, 1, 5, 3, 7]


def mix_rhs(round_i, out_word, bit_in_word):
    """
    Mixed output words after applying:
      (0,1): M0(K0,K1)
      (2,3): M1(K2,K3)
      (4,5): M0(K4,K5)
      (6,7): M1(K6,K7)

    M0(x,y):
      o0 = ROL1(x) XOR y
      o1 = ROL3(y) XOR ROL1(x) XOR y
    M1(x,y):
      o0 = ROL9(x) XOR y
      o1 = ROL28(y) XOR ROL9(x) XOR y
    """
    if out_word in (0, 1):
        xw, yw = 0, 1
        xr = var(round_i, rot_in_word_bitidx(xw, bit_in_word, 1))
        yb = var(round_i, bit_index(yw, bit_in_word))
        if out_word == 0:
            return [xr, yb]
        yr = var(round_i, rot_in_word_bitidx(yw, bit_in_word, 3))
        return [yr, xr, yb]

    if out_word in (2, 3):
        xw, yw = 2, 3
        xr = var(round_i, rot_in_word_bitidx(xw, bit_in_word, 9))
        yb = var(round_i, bit_index(yw, bit_in_word))
        if out_word == 2:
            return [xr, yb]
        yr = var(round_i, rot_in_word_bitidx(yw, bit_in_word, 28))
        return [yr, xr, yb]

    if out_word in (4, 5):
        xw, yw = 4, 5
        xr = var(round_i, rot_in_word_bitidx(xw, bit_in_word, 1))
        yb = var(round_i, bit_index(yw, bit_in_word))
        if out_word == 4:
            return [xr, yb]
        yr = var(round_i, rot_in_word_bitidx(yw, bit_in_word, 3))
        return [yr, xr, yb]

    if out_word in (6, 7):
        xw, yw = 6, 7
        xr = var(round_i, rot_in_word_bitidx(xw, bit_in_word, 9))
        yb = var(round_i, bit_index(yw, bit_in_word))
        if out_word == 6:
            return [xr, yb]
        yr = var(round_i, rot_in_word_bitidx(yw, bit_in_word, 28))
        return [yr, xr, yb]

    raise ValueError("out_word must be in 0..7")


def round_relations(round_i):
    """
    Build equations for the transition K^round_i -> K^(round_i+1).
    """
    relations = []
    perm = perm_words(round_i)  # K^{i+1}[pos] = mixed_out[perm[pos]]
    for pos in range(NWORDS):
        src_out_word = perm[pos]
        for b in range(WORD_BITS):
            out_bit = bit_index(pos, b)
            outv = var(round_i + 1, out_bit)
            rhs = mix_rhs(round_i, src_out_word, b)
            relations.append(" + ".join([outv] + rhs))
    return relations


def write_relationfile(num_rounds=2):
    """
    Build key-schedule relations for `num_rounds` transitions:
      K^0 -> K^1 -> ... -> K^num_rounds

    Fill known/target/not guessed lists manually below.
    """
    if num_rounds < 1:
        raise ValueError("num_rounds must be >= 1 (one transition)")

    cipher_name = "aradi_ks"
    txt = f"#{cipher_name} {num_rounds} Rounds\n"
    txt += "algebraic relations\n"

    for round_i in range(num_rounds):
        for relation in round_relations(round_i):
            txt += relation + "\n"


    known_vars = [var(2, i) for i in range(0, 128)]
    known_vars += [var(1, i) for i in range(128, 256)]
    target_vars = [var(2, i) for i in range(128, 256)]
    not_guessed_vars = [var(0, i) for i in range(128, 256)]
    not_guessed_vars += [var(1, i) for i in range(0, 128)]
    not_guessed_vars += [var(2, i) for i in range(128, 256)]

    txt += "known\n" + "\n".join(known_vars) + "\n"
    txt += "target\n" + "\n".join(target_vars) + "\n"
    txt += "not guessed\n" + "\n".join(not_guessed_vars) + "\n"
    txt += "end"

    path = os.path.join(
        output_dir,
        f"relationfile_{cipher_name}_{num_rounds}r.txt",
    )
    with open(path, "w") as f:
        f.write(txt)



def main():
    write_relationfile()


if __name__ == "__main__":
    main()
