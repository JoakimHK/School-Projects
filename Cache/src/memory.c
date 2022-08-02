/** @file memory.c
 *  @brief Implements starting point for a memory hierarchy with caching and RAM.
 *  @see memory.h
 */


#include "memory.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static unsigned long instr_count;
typedef struct block block_t;
typedef struct set set_t;
typedef struct cache cache_t;
struct cache{
  int cache_size;
  int associativity;
  int block_size;

  unsigned long hits;
  unsigned long misses;

  unsigned long write_hits;
  unsigned long write_misses;

  int n_sets;
  int n_blocks;

  int offset;
  int index_b;

  cache_t *L2;

  set_t **sets;
};

struct set{
  int frequency;
  block_t **blocks;
};


struct block{
  int tag;
  int validBit;
  int frequency;
};

cache_t *L1_inst;
cache_t *L1_data;
cache_t *L2;

void cache_write(cache_t *cache, unsigned int address)
{
  int j = 0;
  int bitMask = pow(2,cache->index_b) - 1;
  int index = (address >> (cache->offset + 2)) & bitMask;
  int tag = address >> (cache->index_b + cache->offset + 2);

  set_t *set = cache->sets[index];
  block_t *block;

  int frequency = set->blocks[0]->frequency;

  for(int i = 0; i < cache->associativity; ++i)
  {
    block = set->blocks[i];
    if(set->blocks[i]->validBit == 0)
    {
      block->tag = tag;
      block->validBit = 1;
      block->frequency = set->frequency;
      ++set->frequency;
      ++cache->write_misses;
      return;

    }

    if(set->blocks[i]->tag == tag && set->blocks[i]->validBit == 1)
    {
      ++cache->write_hits;
      ++set->frequency;
      return;
    }
    

    if(frequency > set->blocks[i]->frequency)
    {
      frequency = set->blocks[i]->frequency;
      j = i;
    }
  }

  block = set->blocks[j];

  block->tag = tag;
  block->validBit = 1;
  ++cache->write_misses;
  ++set->frequency;

  return; 
}


void cache_read(cache_t *cache, unsigned int address)
{
  int bitMask = pow(2,cache->index_b) - 1;
  int index = (address >> (cache->offset + 2)) & bitMask;
  
  set_t *set = cache->sets[index];
  block_t *block;

  int tag = address >> (cache->index_b + cache->offset + 2); //The number 2 equals to the byte offset
  

  for(int i = 0; i < cache->associativity; ++i)
  {
    block = set->blocks[i];
    if(tag == block->tag && block->validBit == 1)
    {
      ++cache->hits;
      block->frequency = set->frequency;
      ++set->frequency;
      return;
    }
  } 
  ++cache->misses;

  if(cache->L2 != NULL) 
  {
    cache_read(cache->L2, address);
  }
  
  cache_write(cache, address);
}


void set_init(set_t *set, int associtivity)
{
  block_t *block;

  set->blocks = calloc(associtivity, sizeof(block_t*));
  if(set->blocks == NULL)
  {
    printf("Did not alocate memory for set blocks");
    goto error;
  }

  for(int i = 0; i < associtivity; ++i)
  {

    block = malloc(sizeof(block_t));
    if(block == NULL)
    {
      printf("Did not alocate memory for block");
      goto error;
    }
    
    block->tag = 0;
    block->validBit = 0;
    set->blocks[i] = block;
  }
  return;

error:
    if(set->blocks != NULL)
    {
      for(int i = 0; i < associtivity; ++i)
      {
        if(set->blocks[i] != NULL)
          free(set->blocks[i]);
      }
      free(set->blocks);
    }
}

void cache_init(cache_t *cache, int cache_size, int associativity, int block_size, cache_t *L2)
{
  set_t *set;

  cache->cache_size = cache_size;
  cache->associativity = associativity;
  cache->block_size = block_size;
  cache->L2 = L2;
  
  cache->n_blocks = cache->cache_size / cache->block_size;
  cache->n_sets = cache->n_blocks / cache->associativity;

  cache->index_b = log2(cache->n_sets);
  cache->offset = log2(cache->block_size/4);

  cache->hits = 0;
  cache->misses = 0;

  cache->write_hits = 0;
  cache->write_misses = 0;


  cache->sets = calloc(cache->n_sets, sizeof(set_t*));
  if(cache->sets == NULL)
  {
    printf("Did not alocate memory for cahce sets");
    goto error;
  }

  for(int i = 0; i < cache->n_sets; ++i)
  {
    set = malloc(sizeof(set_t));
    if(set == NULL)
    {
      printf("Did not alocate memory for set");
      goto error;
    }
    cache->sets[i] = set;
    set_init(cache->sets[i], cache->associativity);
  }
  return;


error:
    if(cache->sets != NULL)
    {
      free(cache->sets);
    }
    free(cache);
  }



void memory_init(void)
{
  L2 = malloc(sizeof(cache_t));
  if(L2 == NULL)
  {
    printf("Did not alocate memory for cahce L2");
    goto error;
  }
  L1_inst = malloc(sizeof(cache_t));
  if(L2 == NULL)
  {
    printf("Did not alocate memory for cahce L1_inst");
    goto error;
  }
  L1_data = malloc(sizeof(cache_t));
  if(L2 == NULL)
  {
    printf("Did not alocate memory for cahce L1_data");
    goto error;
  }
  cache_init(L2, 262144, 8, 256, NULL);
  cache_init(L1_inst, 32768, 4, 256, L2);
  cache_init(L1_data, 32768, 8, 256, L2);

  
  instr_count = 0;

  return;

  error:
    if(L2 != NULL)
    {
      free(L2);
    }
    if(L1_inst != NULL)
    {
      free(L1_inst);
    }
    if(L1_data != NULL)
    {
      free(L1_data);
    }
}

void memory_fetch(unsigned int address, data_t *data)
{
  //printf("memory: fetch 0x%08x\n", address);
  if (data)
  {
    *data = (data_t) 0;
  }

  cache_read(L1_inst, address);

  instr_count++;
}

void memory_read(unsigned int address, data_t *data)
{
  //printf("memory: read 0x%08x\n", address);
  if (data)
    *data = (data_t) 0;


  cache_read(L1_data, address);  
  
  instr_count++;
}

void memory_write(unsigned int address, data_t *data)
{
  //printf("memory: write 0x%08x\n", address);

  cache_write(L1_data, address);
  cache_write(L2, address);
  
  instr_count++;
}

void destroy(cache_t *cache)
{
  set_t *set;
  for(int i = 0; i < cache->n_sets; ++i)
  {
    set = cache->sets[i];
    for(int j = 0; j < cache->associativity; ++j)
    {
      free(set->blocks[j]);
    }
    free(cache->sets[i]);
  }

  free(cache);
}

void memory_finish(void)
{
  fprintf(stdout, "Executed %lu instructions.\n\n", instr_count);

  float L1_inst_total_misses, L1_inst_total_hits, L1_data_total_misses, L1_data_total_hits, L2_total_misses, L2_total_hits;
  

  L1_inst_total_misses = L1_inst->misses + L1_inst->write_misses;
  L1_inst_total_hits = L1_inst->hits + L1_inst->write_hits;

  L1_data_total_misses = L1_data->misses + L1_data->write_misses;
  L1_data_total_hits = L1_data->hits + L1_data->write_hits;

  L2_total_misses = L2->misses + L2->write_misses;
  L2_total_hits = L2->hits + L2->write_hits;

  float L1_inst_missrate = L1_inst_total_misses/(L1_inst_total_hits + L1_inst_total_misses) * 100;
  float L1_data_missrate = L1_data_total_misses/(L1_data_total_hits + L1_data_total_misses) * 100;
  float L2_missrate = L2_total_misses/(L2_total_hits + L2_total_misses) * 100;

  float L1_inst_hitrate = L1_inst_total_hits/(L1_inst_total_hits + L1_inst_total_misses) * 100;
  float L1_data_hitrate = L1_data_total_hits/(L1_data_total_hits + L1_data_total_misses) * 100;
  float L2_hitrate = L2_total_hits/(L2_total_hits + L2_total_misses) * 100;


  printf("L1_inst missrate - %f\n", L1_inst_missrate);
  printf("L1_inst hitrate - %f\n", L1_inst_hitrate);
  printf("L1_inst total misses - %f\n", L1_inst_total_misses);
  printf("L1_inst total hits - %f\n\n", L1_inst_total_hits);

  printf("L1_data missrate - %f\n", L1_data_missrate);
  printf("L1_data hitrate - %f\n", L1_data_hitrate);
  printf("L1_data total misses - %f\n", L1_data_total_misses);
  printf("L1_data total hits - %f\n\n", L1_data_total_hits);

  printf("L2 missrate - %f\n", L2_missrate);
  printf("L2 hitrate - %f\n", L2_hitrate);
  printf("L2 total misses - %f\n", L2_total_misses);
  printf("L2 total hits - %f\n", L2_total_hits);

  destroy(L2);
  destroy(L1_inst);
  destroy(L1_data);
}
