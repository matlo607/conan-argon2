#include "argon2.h"

#include <cstdint>
#include <cstdlib>

#include <algorithm>
#include <array>
#include <iostream>
#include <string>
#include <type_traits>

#define HASHLEN 32
#define SALTLEN 16
#define PASSWORD "password"

template <typename T, std::size_t N>
std::ostream& operator<< (std::ostream& stream, const std::array<T,N>& bytes)
{
    char oldfill = stream.fill();
    stream.fill('0');

    std::ios_base::fmtflags oldff = stream.flags(), ff = oldff;

    ff &= ~std::ios::basefield;   // unset basefield bits
    ff |= std::ios::hex;          // set hex
    ff &= ~std::ios::adjustfield;
    ff |= std::ios::right;
    ff &= ~std::ios::showbase;    // unset showbase

    stream.flags(ff);

    for (auto elt : bytes) {
        if (std::is_same<typename std::remove_cv<T>::type, uint8_t>::value) {
            stream.width(sizeof(T) * 2); // width is not sticky as the other flags
            stream << static_cast<uint16_t>(elt);
        } else {
            stream << elt;
        }
    }

    stream.fill(oldfill);
    stream.flags(oldff);

    return stream;
}

int main(void)
{
    std::string pwd_s = PASSWORD;

    std::array<uint8_t, sizeof(PASSWORD)> pwd = {{0x00}};
    std::transform(pwd_s.begin(), pwd_s.end(), pwd.begin(),
            [](auto c) {
                return static_cast<uint8_t>(c);
            });
    std::array<uint8_t, HASHLEN> hash1;
    std::array<uint8_t, HASHLEN> hash2;

    std::array<uint8_t, SALTLEN> salt = {{0x00}};

    uint32_t t_cost = 2;            // 1-pass computation
    uint32_t m_cost = (1<<16);      // 64 mebibytes memory usage
    uint32_t parallelism = 1;       // number of threads and lanes

    // high-level API
    argon2i_hash_raw(t_cost, m_cost, parallelism,
            pwd.data(), pwd.size(),
            salt.data(), salt.size(),
            hash1.data(), hash1.size());

    // low-level API
    argon2_context context = {
        hash2.data(),  /* output array, at least HASHLEN in size */
        hash2.size(), /* digest length */
        pwd.data(), /* password array */
        pwd.size(), /* password length */
        salt.data(),  /* salt array */
        salt.size(), /* salt length */
        NULL, 0, /* optional secret data */
        NULL, 0, /* optional associated data */
        t_cost, m_cost, parallelism, parallelism,
        ARGON2_VERSION_13, /* algorithm version */
        NULL, NULL, /* custom memory allocation / deallocation functions */
        /* by default only internal memory is cleared (pwd is not wiped) */
        ARGON2_DEFAULT_FLAGS
    };

    int rc = argon2i_ctx( &context );
    if (ARGON2_OK != rc) {
        std::cerr << "Error: " << argon2_error_message(rc) << std::endl;
        exit(1);
    }

    std::cout << hash1 << std::endl;
    if (hash1 != hash2) {
        std::cerr << hash2 << std::endl;
        std::cerr << "fail" << std::endl;
    } else {
        std::cout << "ok" << std::endl;
    }
    return 0;
}
