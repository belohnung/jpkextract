struct JPKFile {
    u8 bruh[22];
    u32 file_len;
    u32 string_len;
    char filename[string_len];
    u8 file[file_len];
  
};
    
JPKFile files[10] @ 0x00; # couldn't figure out how to make it search the entire file lol