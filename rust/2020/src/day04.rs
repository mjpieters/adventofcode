use aoc_runner_derive::aoc;
use std::collections::BTreeMap;
use std::error::Error;
use std::fmt::Display;
use std::str::FromStr;

enum HeightUnit {
    Centimeters,
    Inches,
}

enum EyeColor {
    amb,
    blu,
    brn,
    gry,
    grn,
    hzl,
    oth,
}

enum PassportField {
    BirthYear(u8),
    IssueYear(u8),
    ExpiryYear(u8),
    Height { unit: HeightUnit, amount: u8 },
    HairColor([u8; 3]),
    EyeColor(EyeColor),
    PassportID(u16),
    CountryID,
}

struct PassportRecord {
    fields: BTreeMap<&str, &str>,
}

#[derive(Debug)]
struct PassportRecordParseError;

impl Display for PassportRecordParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("Not a valid passport record")
    }
}

impl Error for PassportRecordParseError {}

impl FromStr for PassportField {
    type Err = InstrParseErr;
    fn from_str(s: &str) -> Result<Self, InstrParseErr> {
        use Instr::*;
        use Ordering::*;
        let line = s.splitn(2, ";").next().unwrap().trim();
        if line.len() == 0 {
            return Err(InstrParseErr(()));
        }
        if line.ends_with(":") {
            return Ok(Label(line.trim_end_matches(":").into()));
        }

        let mut line_parts = line.splitn(2, " ");
        let cmd = line_parts.next().unwrap();
        let args: Vec<_> = match line_parts.next() {
            None => vec![],
            Some(a) => SPLIT_ARGS
                .find_iter(a)
                .map(|m| m.as_str().trim().trim_end_matches(","))
                .collect(),
        };

        match (cmd, args.len()) {
            ("mov", 2) => Ok(Mov(args[0].into(), args[1].into())),
            ("inc", 1) => Ok(Inc(args[0].into())),
            ("dec", 1) => Ok(Dec(args[0].into())),
            ("add", 2) => Ok(Add(args[0].into(), args[1].into())),
            ("sub", 2) => Ok(Sub(args[0].into(), args[1].into())),
            ("mul", 2) => Ok(Mul(args[0].into(), args[1].into())),
            ("div", 2) => Ok(Div(args[0].into(), args[1].into())),
            ("jmp", 1) => Ok(Jmp(JumpInfo::uncond(args[0].into()))),
            ("cmp", 2) => Ok(Cmp(args[0].into(), args[1].into())),
            ("jne", 1) => Ok(Jmp(JumpInfo::new(args[0].into(), |o| o != Equal))),
            ("je", 1) => Ok(Jmp(JumpInfo::new(args[0].into(), |o| o == Equal))),
            ("jge", 1) => Ok(Jmp(JumpInfo::new(args[0].into(), |o| o != Less))),
            ("jg", 1) => Ok(Jmp(JumpInfo::new(args[0].into(), |o| o == Greater))),
            ("jle", 1) => Ok(Jmp(JumpInfo::new(args[0].into(), |o| o != Greater))),
            ("jl", 1) => Ok(Jmp(JumpInfo::new(args[0].into(), |o| o == Less))),
            ("call", 1) => Ok(Call(JumpInfo::uncond(args[0].into()))),
            ("ret", 0) => Ok(Ret),
            ("msg", _) => Ok(Msg(args.iter().map(|&s| MsgPart::from(s)).collect())),
            ("end", 0) => Ok(End),
            _ => Err(InstrParseErr(())),
        }
    }
}
